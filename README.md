
# Espite

**A local language model for compatible ESP32 hardware.**

Espite is an embedded language-model project designed to run inference locally on supported microcontrollers, without requiring cloud APIs, remote inference servers, or a GPU.

## Features

- Local language-model inference
- Decoder-only Transformer architecture
- INT8-quantized model weights
- Grouped-query attention
- Rotary positional embeddings (RoPE)
- RMS normalization
- BPE tokenizer
- PSRAM-backed attention cache
- Serial-based interaction
- No mandatory cloud services

## Model Specifications

| Specification | Value |
|---|---|
| Version | V3.0 |
| Architecture | Decoder-only Transformer |
| Parameter count | 2,047,840 |
| Weight format | INT8 |
| Embedding dimension | 160 |
| Transformer layers | 7 |
| Query attention heads | 5 |
| Key/value attention heads | 1 |
| Head dimension | 32 |
| Feed-forward hidden dimension | 432 |
| Vocabulary size | 1,024 |
| Context window | 384 tokens |
| BPE merge entries | 925 |
| RoPE base | 10,000 |
| Normalization | RMSNorm |
| Normalization epsilon | 0.00001 |

Verify these values against the model header for the exact release.

## Hardware Requirements

Espite does not require a specific development board. Compatibility depends on the microcontroller, memory configuration, firmware, and available flash storage.

### Minimum Requirements

The exact minimum must be confirmed by compiling and running the release on the target board. The following are practical requirements to evaluate:

- An ESP32-family processor supported by the firmware. At best an S3 or Wrover or anything ideally with PSRAM
- Enough flash for the compiled application and embedded model data.
- Enough working RAM for inference, temporary buffers, and runtime state.
- PSRAM if required by the engine's memory-allocation strategy.
- A compatible USB or serial connection for flashing and interaction.

A board having an ESP32 chip does not automatically make it compatible.

The model's theoretical key/value cache alone requires approximately 672 KiB if cached values use four bytes each:

`2 × 7 × 384 × 32 × 4 = 688,128 bytes`

Additional memory is required for other inference operations. Actual requirements depend on the implementation.

### Recommended Requirements

For a more practical setup:

| Component | Recommendation |
|---|---|
| Processor | Supported ESP32-S3 or another compatible ESP32 |
| Flash | 8 MB |
| PSRAM | 2-4 MB |
| USB | Native USB or USB-to-serial |
| Development environment | Arduino IDE with ESP32 board support |

These are recommendations, not requirements to use one particular board.

### Board Compatibility

Potential targets include ESP32-S3 development boards with PSRAM and other ESP32 boards that satisfy the firmware's actual requirements.

Examples include the LilyGO T-Display-S3 and compatible generic ESP32-S3 development boards.

Check the exact processor, flash capacity, PSRAM type, and available memory before attempting to run Espite.

## Project Files

A typical source release may include:

| File | Purpose |
|---|---|
| `Espite.ino` | Arduino entry point and application interface |
| `espite_engine.h` | Inference engine |
| `espite_model.h` | Embedded model weights and metadata |

Use the filenames included in your release. Keep required headers alongside the source files that include them.

Do not combine model and engine files from incompatible releases.

## Installation

### 1. Install Arduino IDE

Download Arduino IDE:

https://www.arduino.cc/en/software

Arduino IDE 2.x is recommended.

### 2. Install ESP32 Board Support

Open **File → Preferences** and add this URL under **Additional Boards Manager URLs**:

`https://espressif.github.io/arduino-esp32/package_esp32_index.json`

Then:

1. Open **Tools → Board → Boards Manager**.
2. Search for `esp32`.
3. Install **esp32 by Espressif Systems**.
4. Restart Arduino IDE if necessary.

Official documentation:

https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html

### 3. Open the Project

1. Download and extract the Espite source.
2. Confirm that the required engine and model files are present.
3. Open the main `.ino` file.
4. Verify that the required headers are recognized.

Do not copy only the `.ino` file if the other files are required.

## Flashing Espite

### Step 1: Connect the Board

Connect the board using a USB data cable.

### Step 2: Select the Board

In Arduino IDE, open **Tools → Board** and select the profile matching your hardware.

For a compatible generic ESP32-S3, `ESP32S3 Dev Module` may be appropriate. Other chips require their corresponding board profiles.

### Step 3: Configure the Hardware

Set the following according to the actual board:

- Flash size
- Flash mode
- PSRAM mode
- CPU frequency
- USB serial configuration
- Partition scheme

Do not assume that every ESP32 board uses the same settings.

### Step 4: Select the Port

Open **Tools → Port** and select the port belonging to your board.

### Step 5: Compile

Click **Verify**.

Check the build output for compilation errors, flash usage, and the final application binary size.

### Step 6: Upload

Click **Upload** and wait for the transfer to complete.

If uploading fails:

- Lower the upload speed.
- Check the selected serial port.
- Check the USB cable.
- Enter download mode if your board requires it.

### Step 7: Open Serial Monitor

Open **Tools → Serial Monitor** and select the baud rate specified by the firmware. Use `115200` if that is the configured rate.

Reset the board if necessary and wait for the startup messages.

## Flash and Partition Configuration

The application partition must be large enough for the compiled firmware binary.

Selecting a 16 MB flash setting does not automatically make the entire chip available to the application.

1. Select the correct physical flash size.
2. Compile Espite.
3. Check the reported binary size.
4. Select a compatible partition large enough for the application.
5. Recompile and upload.

A custom partition table may be necessary if the available presets are too small.

The model header's source-file size is not the same as the compiled binary size. Use the actual build output to determine partition requirements.

## PSRAM Configuration

PSRAM provides additional working memory for inference.

The theoretical key/value cache for the listed architecture is:

`2 × 7 × 384 × 32 × 4 = 688,128 bytes`

This is approximately **672 KiB**, assuming two cached tensors, seven layers, a 384-token context, 32 values per head, and four bytes per value.

This cache is only part of the total memory requirement.

### Enabling PSRAM

1. Open the board settings in Arduino IDE.
2. Locate the PSRAM option.
3. Select the mode supported by the physical board.
4. Compile and upload.
5. Check the startup output for successful PSRAM initialization.

Depending on the hardware, the correct mode may be OPI, QSPI, or another supported configuration.

Do not select a PSRAM mode based only on the processor name. Check the module specifications.




## Memory and Performance

| Memory | Purpose |
|---|---|
| Flash | Firmware and embedded model data |
| Internal SRAM | Runtime state, temporary buffers, and time-critical data |
| PSRAM | Additional capacity for the attention cache and other allocations |

Storing model weights in flash does not eliminate RAM requirements. Inference still requires memory for activations, attention state, and intermediate calculations.

Performance depends on:

- Processor and clock configuration
- Memory bandwidth and PSRAM configuration
- Computation required per token
- Prompt length and active context
- Compiler optimizations
- Generation settings

Measure performance on the actual target hardware. Results from simulators and different boards may vary.

## Troubleshooting

### Application Exceeds the Partition Size

- Verify the physical flash size.
- Select a larger compatible application partition.
- Use a custom partition table if necessary.
- Recompile and confirm that the binary fits.

Increasing the flash-size setting does not automatically enlarge the application partition.

### PSRAM Is Not Detected

- Verify the board and module specifications.
- Select the correct PSRAM mode.
- Confirm the installed board package.
- Run the diagnostic sketch above.

### Model Initialization Fails

- Confirm that all required files are present.
- Check that the engine and model header belong to the same release.
- Inspect serial output for allocation or initialization errors.

### The Board Resets During Inference

Possible causes include failed memory allocation, incorrect PSRAM configuration, a runtime fault, or a watchdog timeout.

1. Capture serial output.
2. Verify PSRAM detection.
3. Check available internal RAM and PSRAM.
4. Test with a short prompt.
5. Investigate the actual error before changing configuration.

### Upload Fails

- Use a USB data cable.
- Select the correct serial port.
- Lower the upload speed.
- Close other applications using the port.
- Enter download mode if required by the board.

The BOOT and RESET procedure varies by development board.

### Serial Monitor Is Blank

- Select the baud rate used by the firmware.
- Confirm the USB serial configuration.
- Press reset after opening Serial Monitor.
- Confirm that the selected port belongs to the board.

## Limitations

Espite is an LLM, therefor it may not be 100% correct thanks to it being...an LLM

- Responses may be incorrect or incomplete.
- Passing a small test set does not establish general accuracy.
- The model may generate plausible but incorrect statements.
- It should not be the sole source for safety-critical decisions.
- Context length, memory usage, and generation speed are constrained by the architecture and hardware.
- Compatibility depends on the exact processor, flash, PSRAM, firmware, and partition configuration.

Local inference avoids a mandatory remote inference service, but does not guarantee privacy against every other component of the device or host system.

## License and Attribution

Follow the license and attribution terms included with the specific Espite release.

Before redistributing source code, model weights, or modified firmware, verify the applicable license and any conditions covering training data and bundled components.

Document modifications and preserve original notices where required.

---

**Espite — local language-model inference on embedded hardware.**
