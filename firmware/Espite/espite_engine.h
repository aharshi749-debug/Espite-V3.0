#pragma once
#include <math.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "espite_model.h"

#define E_D ESPITE_DIM
#define E_L ESPITE_LAYERS
#define E_NH ESPITE_HEADS
#define E_NKV ESPITE_KV_HEADS
#define E_HD (ESPITE_DIM / ESPITE_HEADS)
#define E_KVD (E_NKV * E_HD)
#define E_HID ESPITE_HIDDEN
#define E_V ESPITE_VOCAB
#define E_CTX ESPITE_CTX

#define ESPITE_TOK_USER 1
#define ESPITE_TOK_BOT 2
#define ESPITE_TOK_END 3
#define ESPITE_N_SPECIAL 4
#define ESPITE_BASE (ESPITE_N_SPECIAL + 95)

typedef struct {
  float *kc, *vc;
  int len;
  int turn_start[E_CTX];
  int n_turns;
  uint32_t rng;

  uint32_t last_prefill, last_generated;
} Espite;

static float e_x[E_D], e_xb[E_D], e_xb2[E_D], e_q[E_D];
static float e_hb[E_HID], e_hb2[E_HID], e_att[E_CTX], e_logits[E_V];
static float e_krot[E_CTX * E_KVD];
static float e_rcos[E_CTX * (E_HD / 2)], e_rsin[E_CTX * (E_HD / 2)];

static size_t espite_cache_bytes(void) { return (size_t)2 * E_L * E_CTX * E_KVD * sizeof(float); }

static void espite_init(Espite *e, void *mem, uint32_t seed) {
  e->kc = (float *)mem;
  e->vc = e->kc + (size_t)E_L * E_CTX * E_KVD;
  e->len = 0;
  e->n_turns = 0;
  e->rng = seed ? seed : 0x9E3779B9u;
  for (int p = 0; p < E_CTX; p++)
    for (int i = 0; i < E_HD / 2; i++) {
      double f = pow((double)ESPITE_ROPE_THETA, -2.0 * i / E_HD);
      e_rcos[p * (E_HD / 2) + i] = (float)cos(p * f);
      e_rsin[p * (E_HD / 2) + i] = (float)sin(p * f);
    }
}

static void espite_reset(Espite *e) { e->len = 0; e->n_turns = 0; }

static void e_rmsnorm(float *o, const float *x, const float *w, int n) {
  float ss = 0.f;
  for (int i = 0; i < n; i++) ss += x[i] * x[i];
  ss = 1.0f / sqrtf(ss / n + ESPITE_NORM_EPS);
  for (int i = 0; i < n; i++) o[i] = x[i] * ss * w[i];
}

static void e_matmul(float *out, const float *x, const int8_t *w, const float *s, int n, int d) {
  for (int i = 0; i < d; i++) {
    const int8_t *r = w + (size_t)i * n;
    float a0 = 0.f, a1 = 0.f, a2 = 0.f, a3 = 0.f;
    int j = 0;
    for (; j + 4 <= n; j += 4) {
      a0 += (float)r[j] * x[j];
      a1 += (float)r[j + 1] * x[j + 1];
      a2 += (float)r[j + 2] * x[j + 2];
      a3 += (float)r[j + 3] * x[j + 3];
    }
    for (; j < n; j++) a0 += (float)r[j] * x[j];
    out[i] = (a0 + a1 + a2 + a3) * s[i];
  }
}

static void e_rope(float *v, int pos) {
  const float *c = e_rcos + pos * (E_HD / 2), *s = e_rsin + pos * (E_HD / 2);
  for (int i = 0; i < E_HD / 2; i++) {
    float a = v[2 * i], b = v[2 * i + 1];
    v[2 * i] = a * c[i] - b * s[i];
    v[2 * i + 1] = a * s[i] + b * c[i];
  }
}

static float *espite_forward(Espite *e, int token, int want_logits) {
  const int pos = e->len;
  {
    const int8_t *row = ESPITE_W_EMB + (size_t)token * E_D;
    float sc = ESPITE_S_EMB[token];
    for (int i = 0; i < E_D; i++) e_x[i] = row[i] * sc;
  }
  const float inv_sqrt_hd = 1.0f / sqrtf((float)E_HD);
  for (int l = 0; l < E_L; l++) {
    float *kc = e->kc + (size_t)l * E_CTX * E_KVD;
    float *vc = e->vc + (size_t)l * E_CTX * E_KVD;
    e_rmsnorm(e_xb, e_x, ESPITE_ATTN_NORM + l * E_D, E_D);
    e_matmul(e_q, e_xb, ESPITE_W_WQ + (size_t)l * E_D * E_D, ESPITE_S_WQ + l * E_D, E_D, E_D);
    e_matmul(kc + (size_t)pos * E_KVD, e_xb, ESPITE_W_WK + (size_t)l * E_KVD * E_D, ESPITE_S_WK + l * E_KVD, E_D, E_KVD);
    e_matmul(vc + (size_t)pos * E_KVD, e_xb, ESPITE_W_WV + (size_t)l * E_KVD * E_D, ESPITE_S_WV + l * E_KVD, E_D, E_KVD);

    for (int t = 0; t <= pos; t++) {
      memcpy(e_krot + t * E_KVD, kc + (size_t)t * E_KVD, E_KVD * sizeof(float));
      for (int h = 0; h < E_NKV; h++) e_rope(e_krot + t * E_KVD + h * E_HD, t);
    }
    for (int h = 0; h < E_NH; h++) e_rope(e_q + h * E_HD, pos);

    for (int h = 0; h < E_NH; h++) {
      const int kvh = h / (E_NH / E_NKV);
      const float *qh = e_q + h * E_HD;
      float mx = -1e30f;
      for (int t = 0; t <= pos; t++) {
        const float *kt = e_krot + t * E_KVD + kvh * E_HD;
        float sc = 0.f;
        for (int i = 0; i < E_HD; i++) sc += qh[i] * kt[i];
        sc *= inv_sqrt_hd;
        e_att[t] = sc;
        if (sc > mx) mx = sc;
      }
      float sum = 0.f;
      for (int t = 0; t <= pos; t++) { e_att[t] = expf(e_att[t] - mx); sum += e_att[t]; }
      float *o = e_xb + h * E_HD;
      for (int i = 0; i < E_HD; i++) o[i] = 0.f;
      for (int t = 0; t <= pos; t++) {
        const float a = e_att[t] / sum;
        const float *vt = vc + (size_t)t * E_KVD + kvh * E_HD;
        for (int i = 0; i < E_HD; i++) o[i] += a * vt[i];
      }
    }
    e_matmul(e_xb2, e_xb, ESPITE_W_WO + (size_t)l * E_D * E_D, ESPITE_S_WO + l * E_D, E_D, E_D);
    for (int i = 0; i < E_D; i++) e_x[i] += e_xb2[i];

    e_rmsnorm(e_xb, e_x, ESPITE_FFN_NORM + l * E_D, E_D);
    e_matmul(e_hb, e_xb, ESPITE_W_W1 + (size_t)l * E_HID * E_D, ESPITE_S_W1 + l * E_HID, E_D, E_HID);
    e_matmul(e_hb2, e_xb, ESPITE_W_W3 + (size_t)l * E_HID * E_D, ESPITE_S_W3 + l * E_HID, E_D, E_HID);
    for (int i = 0; i < E_HID; i++) {
      float v = e_hb[i];
      e_hb[i] = v / (1.0f + expf(-v)) * e_hb2[i];
    }
    e_matmul(e_xb, e_hb, ESPITE_W_W2 + (size_t)l * E_D * E_HID, ESPITE_S_W2 + l * E_D, E_HID, E_D);
    for (int i = 0; i < E_D; i++) e_x[i] += e_xb[i];
  }
  e->len++;
  if (!want_logits) return NULL;
  e_rmsnorm(e_x, e_x, ESPITE_FINAL_NORM, E_D);
  e_matmul(e_logits, e_x, ESPITE_W_EMB, ESPITE_S_EMB, E_D, E_V);
  return e_logits;
}

#define ESPITE_PIN_MAX 48
static int espite_evict_turn(Espite *e) {
  if (e->n_turns < 2) return 0;
  int v = (e->n_turns >= 3 && e->turn_start[1] <= ESPITE_PIN_MAX) ? 1 : 0;
  const int from = e->turn_start[v], to = e->turn_start[v + 1], cut = to - from;
  const int tail = e->len - to;
  for (int l = 0; l < E_L; l++) {
    float *kc = e->kc + (size_t)l * E_CTX * E_KVD;
    float *vc = e->vc + (size_t)l * E_CTX * E_KVD;
    memmove(kc + (size_t)from * E_KVD, kc + (size_t)to * E_KVD, (size_t)tail * E_KVD * sizeof(float));
    memmove(vc + (size_t)from * E_KVD, vc + (size_t)to * E_KVD, (size_t)tail * E_KVD * sizeof(float));
  }
  for (int i = v + 1; i < e->n_turns; i++) e->turn_start[i - 1] = e->turn_start[i] - cut;
  e->n_turns--;
  e->len -= cut;
  return 1;
}

static int e_is_alpha(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '\''; }

static int e_merge_rank(int a, int b) {
  uint32_t key = ((uint32_t)a << 16) | (uint32_t)b;
  int lo = 0, hi = ESPITE_N_MERGES - 1;
  while (lo <= hi) {
    int mid = (lo + hi) >> 1;
    uint32_t k = ESPITE_MERGE_KEY[mid];
    if (k == key) return ESPITE_MERGE_RANK[mid];
    if (k < key) lo = mid + 1; else hi = mid - 1;
  }
  return -1;
}

static int e_encode_piece(const char *p, int n, uint16_t *out, int cap) {
  uint16_t ids[128];
  if (n > 128) n = 128;
  for (int i = 0; i < n; i++) ids[i] = (uint16_t)(ESPITE_N_SPECIAL + p[i] - 32);
  while (n > 1) {
    int best = -1, bi = -1;
    for (int i = 0; i + 1 < n; i++) {
      int r = e_merge_rank(ids[i], ids[i + 1]);
      if (r >= 0 && (best < 0 || r < best)) { best = r; bi = i; }
    }
    if (best < 0) break;
    ids[bi] = (uint16_t)(ESPITE_BASE + best);
    memmove(ids + bi + 1, ids + bi + 2, (size_t)(n - bi - 2) * sizeof(uint16_t));
    n--;
  }
  if (n > cap) n = cap;
  memcpy(out, ids, (size_t)n * sizeof(uint16_t));
  return n;
}

static int espite_encode(const char *text, uint16_t *out, int cap) {
  char buf[400];
  int n = 0;
  for (const char *s = text; *s && n < 399; s++) {
    unsigned char c = (unsigned char)*s;
    if (c >= 0x80 && c < 0xC0) continue;
    if (c == '\t' || c == '\n' || c == '\r') c = ' ';
    buf[n++] = (c >= 32 && c <= 126) ? (char)c : '?';
  }
  buf[n] = 0;
  int cnt = 0, i = 0;
  while (i < n && cnt < cap) {
    int j;
    if (buf[i] == ' ' && i + 1 < n && e_is_alpha(buf[i + 1])) {
      j = i + 1;
      while (j < n && e_is_alpha(buf[j])) j++;
    } else if (e_is_alpha(buf[i])) {
      j = i;
      while (j < n && e_is_alpha(buf[j])) j++;
    } else {
      j = i + 1;
    }
    cnt += e_encode_piece(buf + i, j - i, out + cnt, cap - cnt);
    i = j;
  }
  return cnt;
}

static int espite_decode(int tok, char *dst, int cap) {
  int a = ESPITE_VOCAB_OFF[tok], b = ESPITE_VOCAB_OFF[tok + 1];
  int n = b - a;
  if (n > cap - 1) n = cap - 1;
  memcpy(dst, ESPITE_VOCAB_BLOB + a, (size_t)n);
  dst[n] = 0;
  return n;
}

static uint32_t e_rand(Espite *e) {
  uint32_t x = e->rng;
  x ^= x << 13; x ^= x >> 17; x ^= x << 5;
  return e->rng = x;
}

#define E_TOPK 40

static int espite_sample(Espite *e, const float *logits, float temp, float topp) {
  int best = 0;
  for (int i = 1; i < E_V; i++) if (logits[i] > logits[best]) best = i;
  if (temp <= 0.f) return best;
  int idx[E_TOPK]; float val[E_TOPK]; int k = 0;
  for (int i = 0; i < E_V; i++) {
    if (i == 0) continue;
    float v = logits[i];
    if (k < E_TOPK) { idx[k] = i; val[k] = v; k++; }
    else if (v > val[k - 1]) { idx[k - 1] = i; val[k - 1] = v; }
    else continue;
    for (int j = k - 1; j > 0 && val[j] > val[j - 1]; j--) {
      float tv = val[j]; val[j] = val[j - 1]; val[j - 1] = tv;
      int ti = idx[j]; idx[j] = idx[j - 1]; idx[j - 1] = ti;
    }
  }
  const float mx = val[0];
  float sum = 0.f;
  for (int j = 0; j < k; j++) { val[j] = expf((val[j] - mx) / temp); sum += val[j]; }
  float cum = 0.f; int cut = k;
  for (int j = 0; j < k; j++) { cum += val[j] / sum; if (cum >= topp) { cut = j + 1; break; } }
  float tot = 0.f;
  for (int j = 0; j < cut; j++) tot += val[j];
  float r = (e_rand(e) >> 8) * (1.0f / 16777216.0f) * tot;
  for (int j = 0; j < cut; j++) { r -= val[j]; if (r <= 0.f) return idx[j]; }
  return idx[0];
}

typedef void (*espite_emit_fn)(const char *piece, void *user);

static int espite_chat(Espite *e, const char *user_text, float temp, float topp, int max_new,
                       espite_emit_fn emit, void *user) {
  uint16_t in[128];
  char low[400];
  int up = 0, lo = 0, k = 0;
  for (const char *p = user_text; *p; p++) { if (*p >= 'A' && *p <= 'Z') up++; else if (*p >= 'a' && *p <= 'z') lo++; }
  if (up >= 2 && lo == 0) {
    for (; user_text[k] && k < 399; k++) { char c = user_text[k]; low[k] = (c >= 'A' && c <= 'Z') ? (char)(c + 32) : c; }
    low[k] = 0;
    user_text = low;
  }
  int n = espite_encode(user_text, in, 120);
  const int reserve = max_new < 64 ? max_new : 64;
  while (e->len + n + 2 + reserve > E_CTX && espite_evict_turn(e)) {}
  if (e->len + n + 2 + reserve > E_CTX) espite_reset(e);
  e->turn_start[e->n_turns++] = e->len;
  espite_forward(e, ESPITE_TOK_USER, 0);
  for (int i = 0; i < n; i++) espite_forward(e, in[i], 0);
  float *lg = espite_forward(e, ESPITE_TOK_BOT, 1);
  e->last_prefill = (uint32_t)n + 2;
  int gen = 0;
  char piece[48];
  while (gen < max_new) {
    int t = espite_sample(e, lg, temp, topp);
    if (t == ESPITE_TOK_END || t < ESPITE_N_SPECIAL) break;
    espite_decode(t, piece, sizeof piece);
    if (emit) emit(piece, user);
    gen++;
    if (e->len >= E_CTX - 1 && !espite_evict_turn(e)) break;
    lg = espite_forward(e, t, 1);
  }
  if (e->len >= E_CTX) espite_evict_turn(e);
  if (e->len < E_CTX) espite_forward(e, ESPITE_TOK_END, 0);
  e->last_generated = (uint32_t)gen;
  return gen;
}
