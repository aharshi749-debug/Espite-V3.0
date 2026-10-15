ANIMAL_STRUCT_TEXT = r"""
cat | mammal | 2 | 4 | +climb +jump -fly | fish,chicken,mice,meat | meat
kitten | mammal | 1 | 4 | +climb +jump -fly | milk,cat food | meat
dog | mammal | 3 | 4 | +swim +run -fly -climb | meat,dog food | both
puppy | mammal | 2 | 4 | -fly | milk,puppy food | both
lion | mammal | 4 | 4 | +run -fly | meat,zebras,antelopes | meat
tiger | mammal | 4 | 4 | +swim -fly | meat,deer,wild pigs | meat
cheetah | mammal | 3 | 4 | +run -fly | antelopes,hares,meat | meat
caracal | mammal | 3 | 4 | +jump +climb -fly | birds,rabbits,rodents | meat
serval | mammal | 3 | 4 | +jump -fly | rodents,birds,frogs | meat
lynx | mammal | 3 | 4 | +climb -fly | hares,meat | meat
singapura | mammal | 1 | 4 | +climb +jump -fly | cat food | meat
elephant | mammal | 5 | 4 | +swim -fly -climb -jump | grass,leaves,bark,fruit | plant
giraffe | mammal | 5 | 4 | +run -fly -climb | leaves | plant
horse | mammal | 4 | 4 | +run +swim -fly -climb | grass,hay,oats | plant
cow | mammal | 4 | 4 | -fly -climb | grass,hay | plant
pig | mammal | 3 | 4 | +swim -fly -climb | grains,vegetables,fruit | both
sheep | mammal | 3 | 4 | -fly | grass,clover | plant
goat | mammal | 3 | 4 | +climb +jump -fly | grass,leaves,shrubs | plant
chicken | bird | 2 | 2 | -swim | seeds,grains,bugs | both
duck | bird | 2 | 2 | +fly +swim | plants,seeds,bugs,fish | both
owl | bird | 2 | 2 | +fly | mice,insects,birds | meat
eagle | bird | 3 | 2 | +fly | fish,rabbits | meat
penguin | bird | 2 | 2 | -fly +swim | fish,squid,krill | meat
parrot | bird | 2 | 2 | +fly +climb | seeds,nuts,fruit | plant
fish | fish | 1 | 0 | +swim -fly -climb | plants,bugs,fish | both
shark | fish | 4 | 0 | +swim -fly | fish,seals,squid | meat
whale | mammal | 5 | 0 | +swim -fly | krill,fish | meat
dolphin | mammal | 4 | 0 | +swim +jump -fly | fish,squid | meat
octopus | mollusk | 2 | 8 | +swim +climb -fly | crabs,clams,fish | meat
crab | crustacean | 1 | 10 | +swim -fly | algae,worms | both
jellyfish | invertebrate | 1 | 0 | +swim -fly | fish,plankton | meat
frog | amphibian | 1 | 4 | +jump +swim -fly | insects,flies,crickets | meat
snake | reptile | 2 | 0 | +swim +climb -fly | mice,eggs,birds,insects | meat
turtle | reptile | 2 | 4 | +swim -fly -climb | plants,bugs,fish | both
lizard | reptile | 1 | 4 | +climb -fly | insects,bugs | meat
crocodile | reptile | 4 | 4 | +swim -fly -climb | fish,birds,meat | meat
bee | insect | 1 | 6 | +fly | nectar,pollen | plant
ant | insect | 1 | 6 | +climb | seeds,sugar,bugs | both
butterfly | insect | 1 | 6 | +fly | nectar | plant
spider | arachnid | 1 | 8 | +climb -fly | insects,bugs,flies | meat
mouse | mammal | 1 | 4 | +climb -fly | seeds,grains,fruit | plant
rabbit | mammal | 1 | 4 | +jump +dig -fly -climb | grass,hay,carrots,vegetables | plant
hamster | mammal | 1 | 4 | +dig -fly | seeds,grains,veggies | plant
bear | mammal | 4 | 4 | +swim +climb -fly | berries,fish,nuts,honey | both
panda | mammal | 4 | 4 | +climb -fly | bamboo | plant
monkey | mammal | 2 | 4 | +climb +jump -fly | fruit,leaves,insects | both
gorilla | mammal | 4 | 4 | +climb -fly | leaves,stems,fruit | plant
zebra | mammal | 4 | 4 | +run -fly -climb | grass | plant
kangaroo | mammal | 3 | -1 | +jump -fly | grass,leaves | plant
koala | mammal | 2 | 4 | +climb -fly | eucalyptus leaves,leaves | plant
wolf | mammal | 3 | 4 | +run -fly | deer,rabbits,meat | meat
fox | mammal | 2 | 4 | +jump +dig -fly | mice,rabbits,berries,bugs | both
deer | mammal | 3 | 4 | +run +jump +swim -fly | grass,leaves,acorns | plant
squirrel | mammal | 1 | 4 | +climb +jump -fly | nuts,seeds,fruit | plant
bat | mammal | 1 | 2 | +fly | insects,fruit | both
camel | mammal | 4 | 4 | -fly -climb | desert plants,grass | plant
hippo | mammal | 5 | 4 | +swim -fly -climb | grass | plant
dinosaur | reptile | 5 | -1 | | plants,meat | both
"""

NEW_ANIMALS_TEXT = r"""
alligator | alligators | an | An alligator is a big reptile with a wide, rounded snout. Alligators live in the southern United States and China. | Alligators have been around for millions of years. | Alligators eat fish, turtles, birds, and small mammals. | Alligators live in swamps, rivers, and lakes. | Alligators love to bask in the sun and float in the water. | reptile | 4 | 4 | +swim -fly -climb | fish,turtles,birds,meat | meat
raccoon | raccoons | a | A raccoon is a furry animal with a black mask around its eyes and a ringed tail. | Raccoons use their clever front paws like little hands. | Raccoons eat fruit, nuts, bugs, and food from trash cans. | Raccoons live in forests and in cities near people. | Raccoons love to explore at night and dig through trash. | mammal | 2 | 4 | +climb +swim -fly | fruit,nuts,bugs,trash | both
moose | moose | a | A moose is the biggest kind of deer. Male moose have huge, flat antlers. | A moose can be taller than a horse. | Moose eat leaves, twigs, and water plants. | Moose live in cold northern forests. | Moose love to wade into lakes to eat water plants. | mammal | 4 | 4 | +swim -fly -climb | leaves,twigs,plants | plant
flamingo | flamingos | a | A flamingo is a tall pink bird with long legs. | Flamingos are pink because of the shrimp and algae they eat. | Flamingos eat shrimp, algae, and tiny water animals. | Flamingos live in warm lakes and lagoons. | Flamingos love to stand on one leg. | bird | 3 | 2 | +fly | shrimp,algae | both
otter | otters | an | An otter is a playful animal that swims in rivers and the sea. | Sea otters hold hands while they sleep so they don't drift apart. | Otters eat fish, crabs, and clams. | Otters live in rivers, lakes, and along the coast. | Otters love to swim, slide, and play. | mammal | 2 | 4 | +swim -fly | fish,crabs,clams | meat
hedgehog | hedgehogs | a | A hedgehog is a small animal covered in sharp spines. | A hedgehog rolls into a spiky ball when it is scared. | Hedgehogs eat insects, worms, and snails. | Hedgehogs live in gardens, hedges, and woods. | Hedgehogs love to snuffle around at night looking for bugs. | mammal | 1 | 4 | -fly | insects,worms,snails | meat
sloth | sloths | a | A sloth is a slow animal that hangs upside down in trees. | Sloths move so slowly that algae grows on their fur. | Sloths eat leaves. | Sloths live in the rainforests of Central and South America. | Sloths love to hang in trees and sleep. | mammal | 2 | 4 | +climb +swim -fly -run | leaves | plant
platypus | platypuses | a | A platypus is a strange animal from Australia with a bill like a duck. It is a mammal that lays eggs. | A male platypus has a venomous spur on its back legs. | Platypuses eat worms, bugs, and shrimp from the bottom of rivers. | Platypuses live in rivers and streams in Australia. | Platypuses love to dive and hunt underwater. | mammal | 2 | 4 | +swim -fly | worms,bugs,shrimp | meat
llama | llamas | a | A llama is a fluffy animal from South America that people use to carry things. | Llamas sometimes spit when they are upset. | Llamas eat grass and hay. | Llamas live in the Andes Mountains and on farms. | Llamas love to graze and hang out in a herd. | mammal | 4 | 4 | -fly | grass,hay | plant
alpaca | alpacas | an | An alpaca is a fluffy animal like a small llama. People use its soft wool. | Alpaca wool is warmer than sheep wool. | Alpacas eat grass and hay. | Alpacas live in the Andes Mountains and on farms. | Alpacas love to graze together in groups. | mammal | 3 | 4 | -fly | grass,hay | plant
seal | seals | a | A seal is a sea animal with flippers and a smooth, round body. | Seals can hold their breath for a long time while they dive. | Seals eat fish, squid, and shellfish. | Seals live in the ocean and rest on beaches and ice. | Seals love to swim and lie in the sun. | mammal | 3 | -1 | +swim -fly | fish,squid,shellfish | meat
walrus | walruses | a | A walrus is a huge sea animal with long tusks and whiskers. | A walrus uses its tusks to pull itself out of the water. | Walruses eat clams and other shellfish. | Walruses live in the cold Arctic. | Walruses love to rest on the ice in big groups. | mammal | 5 | -1 | +swim -fly | clams,shellfish | meat
beaver | beavers | a | A beaver is a furry animal with big front teeth and a flat tail. | Beavers build dams out of sticks and mud. | Beavers eat bark, twigs, and water plants. | Beavers live in rivers and ponds. | Beavers love to chew wood and build dams. | mammal | 2 | 4 | +swim -fly | bark,twigs,plants,wood | plant
skunk | skunks | a | A skunk is a black and white animal that sprays a stinky smell. | A skunk's spray can be smelled from far away. | Skunks eat insects, worms, fruit, and eggs. | Skunks live in forests, fields, and neighborhoods. | Skunks love to dig for bugs at night. | mammal | 2 | 4 | +dig -fly | insects,worms,fruit,eggs | both
porcupine | porcupines | a | A porcupine is an animal covered in sharp quills. | Porcupines can't shoot their quills, but the quills come off easily. | Porcupines eat bark, leaves, and plants. | Porcupines live in forests. | Porcupines love to climb trees and chew bark. | mammal | 2 | 4 | +climb -fly | bark,leaves,plants | plant
peacock | peacocks | a | A peacock is a male peafowl, a bird with a huge, colorful tail. | A peacock spreads its tail like a fan to show off. | Peacocks eat seeds, bugs, and plants. | Peacocks live in forests in India and in parks. | Peacocks love to show off their tail feathers. | bird | 3 | 2 | +fly | seeds,bugs,plants | both
swan | swans | a | A swan is a large white bird with a long, curved neck. | Swans often stay with the same partner for life. | Swans eat water plants and grass. | Swans live on lakes, ponds, and rivers. | Swans love to glide across the water. | bird | 3 | 2 | +fly +swim | plants,grass | plant
crow | crows | a | A crow is a smart black bird. | Crows can recognize human faces. | Crows eat almost anything, like seeds, bugs, and leftovers. | Crows live almost everywhere, from farms to cities. | Crows love to explore and solve puzzles. | bird | 2 | 2 | +fly | seeds,bugs,leftovers | both
pigeon | pigeons | a | A pigeon is a common gray bird that lives in many cities. | Pigeons can find their way home from far away. | Pigeons eat seeds, grains, and bread crumbs. | Pigeons live in cities, towns, and on cliffs. | Pigeons love to peck for crumbs and coo. | bird | 2 | 2 | +fly | seeds,grains,bread | plant
hummingbird | hummingbirds | a | A hummingbird is a tiny bird that can hover in the air. | A hummingbird's wings beat about fifty times a second. | Hummingbirds drink nectar from flowers and eat tiny bugs. | Hummingbirds live in North and South America. | Hummingbirds love to zip from flower to flower. | bird | 1 | 2 | +fly | nectar,bugs | both
salmon | salmon | a | A salmon is a fish that is born in a river, grows up in the ocean, and swims back to its river to lay eggs. | Salmon can jump up waterfalls. | Salmon eat small fish, shrimp, and insects. | Salmon live in the ocean and in rivers. | Salmon love to swim long distances upstream. | fish | 2 | 0 | +swim +jump -fly | fish,shrimp,insects | meat
seahorse | seahorses | a | A seahorse is a small fish with a head shaped like a horse. | Seahorse dads carry the babies in a pouch. | Seahorses eat tiny shrimp and plankton. | Seahorses live in warm, shallow seas. | Seahorses love to hold onto seaweed with their tails. | fish | 1 | 0 | +swim -fly | shrimp,plankton | meat
starfish | starfish | a | A starfish is a sea animal shaped like a star, usually with five arms. | A starfish can grow back a lost arm. | Starfish eat clams, mussels, and snails. | Starfish live on the ocean floor and in tide pools. | Starfish love to cling to rocks. | invertebrate | 1 | -1 | -fly | clams,mussels,snails | meat
lobster | lobsters | a | A lobster is a sea animal with a hard shell and two big claws. | Lobsters can live for more than fifty years. | Lobsters eat fish, clams, and worms. | Lobsters live on the rocky ocean floor. | Lobsters love to hide in rocky caves. | crustacean | 2 | 10 | +swim -fly | fish,clams,worms | meat
snail | snails | a | A snail is a small, slow animal that carries a spiral shell on its back. | Snails leave a trail of slime to help them move. | Snails eat leaves and plants. | Snails live in gardens, forests, and ponds. | Snails love damp places after the rain. | mollusk | 1 | 0 | +climb -fly -run | leaves,plants | plant
worm | worms | a | A worm is a long, soft animal with no legs that lives in the soil. | Earthworms help plants by mixing and loosening the soil. | Worms eat dead leaves and bits of soil. | Worms live underground in the dirt. | Worms love to wiggle through damp soil. | invertebrate | 1 | 0 | +dig -fly | leaves,soil | plant
ladybug | ladybugs | a | A ladybug is a small round beetle, usually red with black spots. | Ladybugs help gardens by eating tiny pests called aphids. | Ladybugs eat aphids and other tiny bugs. | Ladybugs live in gardens, fields, and forests. | Ladybugs love to crawl on leaves hunting for aphids. | insect | 1 | 6 | +fly +climb | aphids,bugs | meat
dragonfly | dragonflies | a | A dragonfly is a flying insect with a long body and four clear wings. | Dragonflies have been around since before the dinosaurs. | Dragonflies eat mosquitoes and other flying bugs. | Dragonflies live near ponds, lakes, and streams. | Dragonflies love to zoom over the water. | insect | 1 | 6 | +fly | mosquitoes,bugs | meat
grasshopper | grasshoppers | a | A grasshopper is an insect with long back legs for jumping. | Grasshoppers make sounds by rubbing their legs on their wings. | Grasshoppers eat grass and leaves. | Grasshoppers live in fields and meadows. | Grasshoppers love to hop through tall grass. | insect | 1 | 6 | +fly +jump | grass,leaves | plant
chameleon | chameleons | a | A chameleon is a lizard that can change the color of its skin. | A chameleon's eyes can look in two directions at once. | Chameleons eat insects, which they catch with their long, sticky tongue. | Chameleons live in warm forests, mostly in Africa and Madagascar. | Chameleons love to sit still on branches waiting for bugs. | reptile | 1 | 4 | +climb -fly | insects | meat
iguana | iguanas | an | An iguana is a big lizard with a spiky back. | Iguanas can drop their tail to escape and grow a new one. | Iguanas eat leaves, flowers, and fruit. | Iguanas live in warm rainforests and as pets. | Iguanas love to bask in the sun on tree branches. | reptile | 2 | 4 | +climb +swim -fly | leaves,flowers,fruit | plant
toad | toads | a | A toad is an animal like a frog with dry, bumpy skin. | Toads spend more time on land than frogs do. | Toads eat insects, worms, and slugs. | Toads live in gardens, fields, and forests. | Toads love to hide in cool, damp places. | amphibian | 1 | 4 | +jump -fly | insects,worms,slugs | meat
armadillo | armadillos | an | An armadillo is an animal covered in hard, bony plates like armor. | Some armadillos can roll into a ball to protect themselves. | Armadillos eat insects, grubs, and worms. | Armadillos live in the Americas, in grasslands and forests. | Armadillos love to dig for bugs with their claws. | mammal | 2 | 4 | +dig -fly | insects,grubs,worms | meat
badger | badgers | a | A badger is a strong digging animal with a black and white striped face. | Badgers live in underground homes called setts. | Badgers eat worms, insects, roots, and fruit. | Badgers live in woods and fields. | Badgers love to dig tunnels. | mammal | 2 | 4 | +dig -fly | worms,insects,roots,fruit | both
bison | bison | a | A bison is a huge, shaggy animal like a wild cow. | Bison can run as fast as a horse. | Bison eat grass. | Bison live on the open plains of North America. | Bison love to roll in the dust. | mammal | 5 | 4 | +run -fly -climb | grass | plant
chimpanzee | chimpanzees | a | A chimpanzee is a smart ape and one of our closest animal relatives. | Chimpanzees use sticks as tools to catch termites. | Chimpanzees eat fruit, leaves, insects, and sometimes meat. | Chimpanzees live in African forests. | Chimpanzees love to climb, play, and groom each other. | mammal | 3 | -1 | +climb -fly | fruit,leaves,insects | both
orangutan | orangutans | an | An orangutan is a large ape with long arms and orange-red fur. | Orangutans build a new nest in the trees every night. | Orangutans mostly eat fruit, and also leaves and bark. | Orangutans live in the rainforests of Borneo and Sumatra. | Orangutans love to swing through the trees. | mammal | 4 | -1 | +climb -fly | fruit,leaves,bark | plant
lemur | lemurs | a | A lemur is a small primate with big eyes and a long tail. | Lemurs only live in the wild on the island of Madagascar. | Lemurs eat fruit, leaves, and flowers. | Lemurs live in the forests of Madagascar. | Lemurs love to leap from tree to tree. | mammal | 2 | 4 | +climb +jump -fly | fruit,leaves,flowers | plant
meerkat | meerkats | a | A meerkat is a small animal from Africa that stands up on its back legs to look around. | Meerkats take turns standing guard for their group. | Meerkats eat insects, scorpions, and lizards. | Meerkats live in deserts and grasslands in southern Africa. | Meerkats love to dig burrows and sunbathe. | mammal | 1 | 4 | +dig -fly | insects,scorpions,lizards | meat
mole | moles | a | A mole is a small animal that lives underground and digs tunnels. | Moles have tiny eyes and can barely see. | Moles eat worms and insects. | Moles live underground in fields and gardens. | Moles love to dig tunnels with their big front paws. | mammal | 1 | 4 | +dig -fly | worms,insects | meat
opossum | opossums | an | An opossum is a small animal with a pointy face and a long tail. Mothers carry their babies in a pouch. | Opossums sometimes play dead when they are scared. | Opossums eat fruit, insects, eggs, and leftovers. | Opossums live in forests and neighborhoods in the Americas. | Opossums love to explore at night. | mammal | 2 | 4 | +climb -fly | fruit,insects,eggs | both
hyena | hyenas | a | A hyena is a wild animal from Africa that looks a bit like a dog. | Spotted hyenas make a sound that sounds like laughing. | Hyenas eat meat, from hunting and from leftovers. | Hyenas live in the grasslands of Africa. | Hyenas love to hunt in groups. | mammal | 3 | 4 | +run -fly | meat | meat
jaguar | jaguars | a | A jaguar is a big wild cat with spots shaped like rings. | Jaguars have one of the strongest bites of any cat. | Jaguars eat deer, fish, and caimans. | Jaguars live in the rainforests of Central and South America. | Jaguars love to swim and hunt near rivers. | mammal | 4 | 4 | +swim +climb -fly | deer,fish,meat | meat
leopard | leopards | a | A leopard is a big wild cat with spotted fur. | Leopards drag their food up into trees to keep it safe. | Leopards eat antelopes, monkeys, and other animals. | Leopards live in Africa and Asia. | Leopards love to rest on tree branches. | mammal | 4 | 4 | +climb -fly | antelopes,monkeys,meat | meat
cougar | cougars | a | A cougar is a big wild cat with tan fur, also called a mountain lion. | Cougars can leap very far in a single jump. | Cougars eat deer and other animals. | Cougars live in mountains and forests in the Americas. | Cougars love to hunt quietly at dawn and dusk. | mammal | 4 | 4 | +jump +climb -fly | deer,meat | meat
ostrich | ostriches | an | An ostrich is the biggest bird in the world. It cannot fly, but it runs very fast. | Ostriches lay the biggest eggs of any bird. | Ostriches eat plants, seeds, and bugs. | Ostriches live in the grasslands and deserts of Africa. | Ostriches love to run across open land. | bird | 4 | 2 | -fly +run | plants,seeds,bugs | both
pelican | pelicans | a | A pelican is a big water bird with a huge pouch under its bill. | Pelicans scoop up fish with their pouch. | Pelicans eat fish. | Pelicans live near coasts, lakes, and rivers. | Pelicans love to dive for fish. | bird | 3 | 2 | +fly +swim | fish | meat
seagull | seagulls | a | A seagull is a gray and white bird that lives near the sea. | Seagulls are very good at stealing food. | Seagulls eat fish, crabs, and leftover food. | Seagulls live near beaches and coasts. | Seagulls love to glide over the waves. | bird | 2 | 2 | +fly +swim | fish,crabs,leftovers | both
woodpecker | woodpeckers | a | A woodpecker is a bird that pecks holes in trees with its strong beak. | A woodpecker can peck about twenty times a second. | Woodpeckers eat insects that live in wood, plus nuts and seeds. | Woodpeckers live in forests and woods. | Woodpeckers love to drum on trees. | bird | 1 | 2 | +fly +climb | insects,nuts,seeds | both
robin | robins | a | A robin is a small bird with a red or orange chest. | Robins are often one of the first birds to sing in the morning. | Robins eat worms, insects, and berries. | Robins live in gardens, parks, and woods. | Robins love to hop on lawns looking for worms. | bird | 1 | 2 | +fly | worms,insects,berries | both
hawk | hawks | a | A hawk is a bird of prey with sharp eyes and strong claws. | Hawks can spot a mouse from high in the sky. | Hawks eat mice, rabbits, snakes, and small birds. | Hawks live in forests, fields, and deserts. | Hawks love to circle high in the sky looking for food. | bird | 2 | 2 | +fly | mice,rabbits,snakes,meat | meat
falcon | falcons | a | A falcon is a fast bird of prey. | The peregrine falcon is the fastest animal on Earth when it dives. | Falcons eat other birds and small animals. | Falcons live on cliffs, in open land, and even on tall city buildings. | Falcons love to dive at amazing speeds. | bird | 2 | 2 | +fly | birds,meat | meat
vulture | vultures | a | A vulture is a large bird that eats animals that have already died. | Vultures help keep nature clean. | Vultures eat dead animals. | Vultures live in open lands, deserts, and mountains. | Vultures love to soar high on warm air. | bird | 3 | 2 | +fly | meat | meat
turkey | turkeys | a | A turkey is a large bird with a red, fleshy neck. Wild turkeys live in North American forests. | Wild turkeys can fly short distances and sleep in trees. | Turkeys eat seeds, nuts, berries, and insects. | Turkeys live in forests and on farms. | Turkeys love to scratch the ground looking for food. | bird | 3 | 2 | +run | seeds,nuts,berries,insects | both
goose | geese | a | A goose is a large bird that swims and honks loudly. | Geese fly in a V shape when they migrate. | Geese eat grass, seeds, and water plants. | Geese live near lakes, ponds, and parks. | Geese love to honk and swim in groups. | bird | 3 | 2 | +fly +swim | grass,seeds,plants | plant
donkey | donkeys | a | A donkey is an animal like a small horse with long ears. | Donkeys are very strong and have great memories. | Donkeys eat grass, hay, and straw. | Donkeys live on farms and in dry, hilly lands. | Donkeys love to graze and roll in the dust. | mammal | 3 | 4 | -fly -climb | grass,hay,straw | plant
reindeer | reindeer | a | A reindeer is a deer that lives in cold places. Both males and females grow antlers. | Reindeer can see ultraviolet light. | Reindeer eat lichen, grass, and leaves. | Reindeer live in the cold Arctic. | Reindeer love to travel in big herds. | mammal | 4 | 4 | +swim +run -fly | lichen,grass,leaves | plant
antelope | antelopes | an | An antelope is a fast, graceful animal with horns, like a deer. | Some antelopes can run faster than eighty kilometers per hour. | Antelopes eat grass and leaves. | Antelopes live in the grasslands of Africa and Asia. | Antelopes love to run and leap across the plains. | mammal | 3 | 4 | +run +jump -fly | grass,leaves | plant
gazelle | gazelles | a | A gazelle is a small, fast antelope. | Gazelles leap high in the air when they run from danger. | Gazelles eat grass and leaves. | Gazelles live in the grasslands of Africa and Asia. | Gazelles love to bound across the plains. | mammal | 3 | 4 | +run +jump -fly | grass,leaves | plant
rhino | rhinos | a | A rhino is a huge animal with thick skin and one or two horns on its nose. | A rhino's horn is made of the same stuff as your fingernails. | Rhinos eat grass, leaves, and shrubs. | Rhinos live in Africa and Asia. | Rhinos love to take mud baths. | mammal | 5 | 4 | +run -fly -climb | grass,leaves,shrubs | plant
manatee | manatees | a | A manatee is a big, gentle sea animal, sometimes called a sea cow. | Manatees can hold their breath for about twenty minutes. | Manatees eat sea grass and water plants. | Manatees live in warm coastal waters and rivers. | Manatees love to float slowly and munch on plants. | mammal | 5 | 0 | +swim -fly | sea grass,plants | plant
orca | orcas | an | An orca, also called a killer whale, is a big black and white dolphin. | Orcas hunt in family groups called pods. | Orcas eat fish, seals, and squid. | Orcas live in oceans all over the world. | Orcas love to swim fast and hunt together. | mammal | 5 | 0 | +swim +jump -fly | fish,seals,squid | meat
narwhal | narwhals | a | A narwhal is a whale with a long, spiral tusk. | A narwhal's tusk is actually a very long tooth. | Narwhals eat fish, shrimp, and squid. | Narwhals live in the cold Arctic ocean. | Narwhals love to swim in groups among the ice. | mammal | 4 | 0 | +swim -fly | fish,shrimp,squid | meat
squid | squids | a | A squid is a sea animal with a long body, eight arms, and two tentacles. | Squids squirt ink to escape from danger. | Squids eat fish and shrimp. | Squids live in oceans all over the world. | Squids love to zoom through the water. | mollusk | 2 | -1 | +swim -fly | fish,shrimp | meat
clam | clams | a | A clam is a sea animal that lives inside two hard shells. | Some giant clams can live for more than one hundred years. | Clams eat tiny bits of food they filter from the water. | Clams live buried in sand and mud under the water. | Clams love to stay hidden in the sand. | mollusk | 1 | 0 | -fly -run | plankton | both
shrimp | shrimp | a | A shrimp is a small sea animal with a long body and many legs. | Some shrimp clean other fish by eating dirt off them. | Shrimp eat tiny plants, animals, and bits of food. | Shrimp live in oceans, rivers, and lakes. | Shrimp love to swim along the bottom. | crustacean | 1 | 10 | +swim -fly | plants,plankton | both
stingray | stingrays | a | A stingray is a flat fish with a long tail that can sting. | Stingrays are related to sharks. | Stingrays eat clams, shrimp, and worms. | Stingrays live on sandy ocean floors. | Stingrays love to glide along the bottom of the sea. | fish | 3 | 0 | +swim -fly | clams,shrimp,worms | meat
eel | eels | an | An eel is a long, slippery fish that looks like a snake. | Electric eels can make a strong shock. | Eels eat fish, worms, and crabs. | Eels live in rivers and the ocean. | Eels love to hide in rocks and mud. | fish | 2 | 0 | +swim -fly | fish,worms,crabs | meat
goldfish | goldfish | a | A goldfish is a small orange fish that many people keep as a pet. | Goldfish can live for more than ten years with good care. | Goldfish eat fish flakes, plants, and tiny bugs. | Goldfish live in ponds, tanks, and bowls. | Goldfish love to swim around and explore their tank. | fish | 1 | 0 | +swim -fly | fish flakes,plants,bugs | both
piranha | piranhas | a | A piranha is a fish from South America with very sharp teeth. | Most piranhas are actually shy and eat plants too. | Piranhas eat fish, insects, seeds, and plants. | Piranhas live in rivers in South America. | Piranhas love to swim in groups. | fish | 1 | 0 | +swim -fly | fish,insects,seeds,plants | both
catfish | catfish | a | A catfish is a fish with long whiskers that look like a cat's. | Catfish can taste food with their whole body. | Catfish eat bugs, worms, and smaller fish. | Catfish live in rivers, lakes, and ponds. | Catfish love to search the muddy bottom for food. | fish | 2 | 0 | +swim -fly | bugs,worms,fish | both
tadpole | tadpoles | a | A tadpole is a baby frog that lives in water and has a tail. | Tadpoles grow legs and lose their tails as they turn into frogs. | Tadpoles eat algae and tiny plants. | Tadpoles live in ponds and puddles. | Tadpoles love to wiggle through the water. | amphibian | 1 | 0 | +swim -fly | algae,plants | plant
salamander | salamanders | a | A salamander is an animal that looks like a lizard but has smooth, wet skin. | Some salamanders can grow back lost legs. | Salamanders eat worms, insects, and slugs. | Salamanders live in damp forests and near streams. | Salamanders love to hide under logs and rocks. | amphibian | 1 | 4 | +swim -fly | worms,insects,slugs | meat
gecko | geckos | a | A gecko is a small lizard that can climb walls and even ceilings. | Geckos lick their own eyes to keep them clean. | Geckos eat insects. | Geckos live in warm places, including houses. | Geckos love to climb walls at night hunting bugs. | reptile | 1 | 4 | +climb -fly | insects | meat
tortoise | tortoises | a | A tortoise is a turtle that lives only on land. | Some tortoises can live for more than one hundred and fifty years. | Tortoises eat grass, leaves, and flowers. | Tortoises live in deserts, grasslands, and forests. | Tortoises love to munch on plants and sunbathe. | reptile | 2 | 4 | -fly -climb -run | grass,leaves,flowers | plant
cobra | cobras | a | A cobra is a venomous snake that can spread a hood around its neck. | Some cobras can spit venom. | Cobras eat rats, frogs, birds, and other snakes. | Cobras live in Africa and Asia. | Cobras love to rest in warm, hidden spots. | reptile | 2 | 0 | -fly | rats,frogs,birds,snakes | meat
scorpion | scorpions | a | A scorpion is a small animal with eight legs, two pincers, and a stinger on its tail. | Scorpions glow under ultraviolet light. | Scorpions eat insects and spiders. | Scorpions live in deserts and warm places. | Scorpions love to hide under rocks during the day. | arachnid | 1 | 8 | -fly | insects,spiders | meat
beetle | beetles | a | A beetle is an insect with hard wing covers on its back. | There are more kinds of beetles than any other animal. | Beetles eat plants, wood, and other bugs. | Beetles live almost everywhere on land. | Beetles love to crawl around looking for food. | insect | 1 | 6 | +fly | plants,wood,bugs | both
mosquito | mosquitoes | a | A mosquito is a small flying insect. Female mosquitoes bite to drink blood. | Mosquitoes find people by smelling the air we breathe out. | Mosquitoes drink plant nectar, and females also drink blood. | Mosquitoes live near water almost everywhere. | Mosquitoes love warm, wet places. | insect | 1 | 6 | +fly | nectar,blood | both
firefly | fireflies | a | A firefly is a beetle that makes its own light. | Fireflies blink their lights to talk to each other. | Fireflies eat nectar, and their babies eat snails and worms. | Fireflies live in fields and woods. | Fireflies love to glow on warm summer nights. | insect | 1 | 6 | +fly | nectar,snails,worms | both
wasp | wasps | a | A wasp is a flying insect with a narrow waist that can sting. | Some wasps build paper nests by chewing wood. | Wasps eat other insects and sweet nectar. | Wasps live in nests in trees, in the ground, and on buildings. | Wasps love to buzz around sweet food. | insect | 1 | 6 | +fly | insects,nectar | both
termite | termites | a | A termite is a small insect that eats wood. | Termites build giant mounds that can be taller than a person. | Termites eat wood and plants. | Termites live in colonies in mounds and wood. | Termites love to chew through wood. | insect | 1 | 6 | +dig | wood,plants | plant
caterpillar | caterpillars | a | A caterpillar is a baby butterfly or moth. It looks like a fuzzy worm with lots of legs. | A caterpillar turns into a butterfly inside a chrysalis. | Caterpillars eat leaves. | Caterpillars live on plants. | Caterpillars love to munch on leaves all day. | insect | 1 | -1 | -fly +climb | leaves | plant
guinea pig | guinea pigs | a | A guinea pig is a small, chubby pet with no tail. | Guinea pigs squeak loudly when they are excited. | Guinea pigs eat hay, vegetables, and fruit. | Guinea pigs live in cages as pets. | Guinea pigs love to munch on hay and squeak. | mammal | 1 | 4 | -fly -climb | hay,vegetables,fruit | plant
ferret | ferrets | a | A ferret is a long, slim, playful pet. | Ferrets sleep up to eighteen hours a day. | Ferrets eat meat. | Ferrets live as pets in homes. | Ferrets love to play and hide in small spaces. | mammal | 1 | 4 | -fly | meat | meat
gerbil | gerbils | a | A gerbil is a small pet rodent with a long tail. | Gerbils thump their back feet to warn others. | Gerbils eat seeds, grains, and vegetables. | Gerbils live in deserts in the wild and in cages as pets. | Gerbils love to dig and build tunnels. | mammal | 1 | 4 | +dig -fly | seeds,grains,vegetables | plant
pony | ponies | a | A pony is a small type of horse. | Ponies are often stronger for their size than horses. | Ponies eat grass and hay. | Ponies live on farms and in fields. | Ponies love to graze and run. | mammal | 3 | 4 | +run -fly -climb | grass,hay | plant
polar bear | polar bears | a | A polar bear is a big white bear that lives in the Arctic. | A polar bear's skin is actually black under its white fur. | Polar bears eat seals. | Polar bears live on the sea ice in the Arctic. | Polar bears love to swim and hunt seals. | mammal | 4 | 4 | +swim -fly | seals,meat | meat
wombat | wombats | a | A wombat is a small, strong animal from Australia that digs burrows. | Wombat poop is shaped like little cubes. | Wombats eat grass, roots, and bark. | Wombats live in burrows in Australia. | Wombats love to dig. | mammal | 2 | 4 | +dig -fly | grass,roots,bark | plant
axolotl | axolotls | an | An axolotl is a salamander from Mexico that keeps its feathery gills its whole life. | Axolotls can regrow lost legs and even parts of their heart. | Axolotls eat worms, insects, and small fish. | Axolotls live in lakes in Mexico and in tanks. | Axolotls love to sit on the bottom of the water. | amphibian | 1 | 4 | +swim -fly | worms,insects,fish | meat
tapir | tapirs | a | A tapir is an animal like a pig with a short, bendy snout. | A tapir uses its snout like a tiny trunk to grab leaves. | Tapirs eat leaves, fruit, and water plants. | Tapirs live in forests in South America and Asia. | Tapirs love to swim and wallow in water. | mammal | 4 | 4 | +swim -fly | leaves,fruit,plants | plant
mongoose | mongooses | a | A mongoose is a small, quick animal that is famous for fighting snakes. | Some mongooses can survive snake venom. | Mongooses eat insects, crabs, snakes, and eggs. | Mongooses live in Africa and Asia. | Mongooses love to hunt and dig. | mammal | 1 | 4 | +dig -fly | insects,crabs,snakes,eggs | meat
yak | yaks | a | A yak is a big, hairy animal like a cow that lives in the mountains. | Yaks can live high up where the air is thin. | Yaks eat grass and moss. | Yaks live in the Himalayas and Tibet. | Yaks love to graze on cold mountain slopes. | mammal | 4 | 4 | +climb -fly | grass,moss | plant
hare | hares | a | A hare is an animal like a big rabbit with long ears and strong back legs. | Hares are born with fur and open eyes. | Hares eat grass, herbs, and bark. | Hares live in fields and open land. | Hares love to run and leap. | mammal | 2 | 4 | +run +jump -fly | grass,herbs,bark | plant
swordfish | swordfish | a | A swordfish is a big fish with a long, flat bill shaped like a sword. | Swordfish are among the fastest fish in the sea. | Swordfish eat fish and squid. | Swordfish live in warm oceans. | Swordfish love to swim fast in the open sea. | fish | 4 | 0 | +swim -fly | fish,squid | meat
sea turtle | sea turtles | a | A sea turtle is a turtle that lives in the ocean and has flippers. | Sea turtles return to the beach where they were born to lay eggs. | Sea turtles eat jellyfish, sea grass, and crabs. | Sea turtles live in warm oceans. | Sea turtles love to swim long distances. | reptile | 3 | 4 | +swim -fly | jellyfish,sea grass,crabs | both
komodo dragon | komodo dragons | a | A Komodo dragon is the biggest lizard in the world. | Komodo dragons can smell food from far away with their tongue. | Komodo dragons eat deer, pigs, and other animals. | Komodo dragons live on a few islands in Indonesia. | Komodo dragons love to lie in the sun. | reptile | 4 | 4 | +swim -fly | deer,pigs,meat | meat
bobcat | bobcats | a | A bobcat is a wild cat with a short tail and tufted ears. | Bobcats are about twice the size of a house cat. | Bobcats eat rabbits, birds, and mice. | Bobcats live in forests and deserts in North America. | Bobcats love to hunt at dawn and dusk. | mammal | 2 | 4 | +climb +jump -fly | rabbits,birds,mice | meat
puffin | puffins | a | A puffin is a small seabird with a colorful beak. | Puffins can carry many fish in their beak at once. | Puffins eat small fish. | Puffins live on cliffs by the cold northern seas. | Puffins love to dive for fish. | bird | 1 | 2 | +fly +swim | fish | meat
pangolin | pangolins | a | A pangolin is an animal covered in hard scales that eats ants. | Pangolins roll into a tight ball when they are scared. | Pangolins eat ants and termites with their long, sticky tongue. | Pangolins live in Africa and Asia. | Pangolins love to dig into ant nests. | mammal | 2 | 4 | +dig +climb -fly | ants,termites | meat
"""

NEW_TOPICS_TEXT = r"""
eye | eyes | an | An eye is the part of the body you see with. | Your eyes blink about fifteen times a minute. | We use our eyes to see.
ear | ears | an | An ear is the part of the body you hear with. | Your ears also help you keep your balance. | We use our ears to hear.
nose | noses | a | A nose is the part of your face you smell and breathe with. | Your nose can tell apart thousands of smells. | We use our nose to smell and breathe.
mouth | mouths | a | A mouth is the part of your face you eat and talk with. | Your mouth makes spit to help you swallow food. | We use our mouth to eat, talk, and smile.
tooth | teeth | a | A tooth is one of the hard white parts in your mouth used for biting and chewing. | Tooth enamel is the hardest thing in the human body. | We use our teeth to bite and chew food.
hand | hands | a | A hand is the part at the end of your arm with fingers and a thumb. | Each hand has twenty seven bones. | We use our hands to hold, write, and build things.
foot | feet | a | A foot is the part at the end of your leg that you stand on. | Each foot has twenty six bones. | We use our feet to stand, walk, and run.
skin | - | - | Skin is the outer covering of your body. It protects you. | Skin is the biggest organ in the human body. | Skin protects the body and helps you feel touch.
lung | lungs | a | A lung is an organ in your chest that breathes air in and out. You have two lungs. | Your lungs take in oxygen and get rid of carbon dioxide. | We use our lungs to breathe.
stomach | stomachs | a | A stomach is the organ where your food gets broken down after you swallow it. | Your stomach makes acid to help digest food. | The stomach is used to digest food.
hair | - | - | Hair is made of thin strands that grow from your skin. | Hair grows about one centimeter a month. | Hair helps keep you warm and protects your skin.
muscle | muscles | a | A muscle is a part of your body that pulls to make you move. | You have more than six hundred muscles. | We use our muscles to move, lift, and run.
weather | - | the | The weather is what the air outside is like, such as sunny, rainy, or windy. | Scientists who study the weather are called meteorologists. | -
storm | storms | a | A storm is strong weather with wind, rain, and sometimes thunder and lightning. | Big storms can knock down trees and power lines. | -
tornado | tornadoes | a | A tornado is a spinning column of air that reaches down from a storm cloud. | Tornado winds can be faster than three hundred kilometers per hour. | -
hurricane | hurricanes | a | A hurricane is a huge, spinning storm that forms over warm oceans. | Hurricanes are given names, like people. | -
fog | - | - | Fog is a cloud that sits close to the ground. | Fog forms when warm, wet air cools down. | -
season | seasons | a | A season is a part of the year with its own weather, like summer or winter. | There are four seasons: spring, summer, fall, and winter. | -
summer | - | - | Summer is the warmest season of the year. | Summer days are longer than winter days. | -
winter | - | - | Winter is the coldest season of the year. | In some places it snows in winter. | -
soccer | - | - | Soccer is a sport where two teams kick a ball and try to score goals. | Soccer is the most popular sport in the world. | -
basketball | - | - | Basketball is a sport where teams try to throw a ball through a high hoop. | Basketball was invented in 1891. | -
baseball | - | - | Baseball is a sport where players hit a ball with a bat and run around four bases. | A baseball game has nine innings. | -
football | - | - | Football is a sport where teams carry or throw a ball to score touchdowns. In many countries, football means soccer. | An American football field is one hundred yards long. | -
tennis | - | - | Tennis is a sport where players hit a ball over a net with rackets. | Tennis can be played by two or four players. | -
chess | - | - | Chess is a board game where two players move pieces to trap the other player's king. | The most powerful chess piece is the queen. | -
swimming | - | - | Swimming is moving through water using your arms and legs. | Swimming is great exercise for your whole body. | -
golf | - | - | Golf is a sport where players hit a small ball into holes using clubs. | In golf, the fewer hits it takes, the better. | -
firefighter | firefighters | a | A firefighter is a person who puts out fires and rescues people. | Firefighters wear special gear to protect them from heat. | -
police officer | police officers | a | A police officer is a person whose job is to keep people safe and enforce the law. | In an emergency, you can call the police for help. | -
nurse | nurses | a | A nurse is a person who cares for sick and hurt people. | Nurses work in hospitals, schools, and clinics. | -
chef | chefs | a | A chef is a person who cooks food as a job. | A head chef is in charge of a whole kitchen. | -
pilot | pilots | a | A pilot is a person who flies planes or helicopters. | Pilots train for many hours before flying passengers. | -
farmer | farmers | a | A farmer is a person who grows crops or raises animals. | Farmers grow most of the food we eat. | -
programmer | programmers | a | A programmer is a person who writes code for computers. | Programmers spend a lot of time finding and fixing bugs. | -
astronaut | astronauts | an | An astronaut is a person who travels into space. | Astronauts float in space because they are falling around the Earth. | -
mechanic | mechanics | a | A mechanic is a person who fixes cars and machines. | Mechanics use tools like wrenches and jacks. | -
bus | buses | a | A bus is a big vehicle that carries lots of people. | School buses are yellow so they are easy to see. | Buses are used to carry many people around a city or to school.
truck | trucks | a | A truck is a big vehicle that carries heavy things. | Some trucks have eighteen wheels. | Trucks are used to carry heavy loads.
helicopter | helicopters | a | A helicopter is an aircraft with spinning blades on top that can fly straight up. | Helicopters can hover in one spot. | Helicopters are used for rescues, news, and flying where planes can't land.
motorcycle | motorcycles | a | A motorcycle is a two-wheeled vehicle with an engine. | Riders wear helmets to stay safe. | Motorcycles are used to travel quickly on roads.
submarine | submarines | a | A submarine is a boat that can travel underwater. | Submarines use tanks of water and air to sink and rise. | Submarines are used to explore and travel under the sea.
tractor | tractors | a | A tractor is a strong farm vehicle with big wheels. | Tractors can pull plows and heavy trailers. | Tractors are used to plow fields and pull farm machines.
violin | violins | a | A violin is a small musical instrument with four strings that you play with a bow. | Violins are usually made of wood. | Violins are used to play music.
trumpet | trumpets | a | A trumpet is a brass instrument that you blow into. | Trumpets have three valves to change notes. | Trumpets are used to play loud, bright music.
flute | flutes | a | A flute is a musical instrument you play by blowing across a hole. | Flutes are one of the oldest instruments. | Flutes are used to play music.
geography | - | - | Geography is the study of places, maps, and the land and people of Earth. | Geography helps you understand where countries and cities are. | -
biology | - | - | Biology is the study of living things. | Biology includes plants, animals, and tiny cells. | -
mango | mangoes | a | A mango is a sweet, juicy tropical fruit with orange flesh. | Mangoes grow on big trees in warm places. | -
pineapple | pineapples | a | A pineapple is a sweet tropical fruit with spiky skin and a leafy top. | A pineapple takes about two years to grow. | -
avocado | avocados | an | An avocado is a green fruit with a big seed and creamy flesh. | Guacamole is made from avocados. | -
broccoli | - | - | Broccoli is a green vegetable that looks like a tiny tree. | Broccoli is full of vitamins. | -
onion | onions | an | An onion is a vegetable with layers that grows underground. | Cutting onions can make you cry. | -
noodle | noodles | a | A noodle is a long, thin strip of dough that you cook in water or soup. | People have eaten noodles for thousands of years. | -
donut | donuts | a | A donut is a sweet fried dough snack, often shaped like a ring. | Donuts are often covered in glaze or sprinkles. | -
waffle | waffles | a | A waffle is a crispy breakfast food with little square pockets. | Waffles are cooked in a special iron. | -
pie | pies | a | A pie is a baked food with a crust and a filling, like fruit. | Apple pie is one of the most popular pies. | -
yogurt | - | - | Yogurt is a creamy food made from milk. | Yogurt is made with good bacteria. | -
peanut | peanuts | a | A peanut is a small seed that grows underground in a shell. | Peanut butter is made from ground peanuts. | -
corn | - | - | Corn is a grain that grows on tall plants as yellow kernels on a cob. | Popcorn is made from a special kind of corn. | -
multimeter | multimeters | a | A multimeter is a tool that measures voltage, current, and resistance. | Many multimeters beep when a circuit is connected. | Multimeters are used to test and fix circuits.
oscilloscope | oscilloscopes | an | An oscilloscope is a tool that draws electrical signals as waves on a screen. | Oscilloscopes can show signals that change millions of times a second. | Oscilloscopes are used to see and debug electronic signals.
soldering iron | soldering irons | a | A soldering iron is a hot tool that melts solder to join electronic parts. | The tip of a soldering iron can get hotter than three hundred degrees Celsius. | Soldering irons are used to connect parts to circuit boards.
infrared | - | - | Infrared is a kind of light that our eyes can't see. TV remotes use it. | You can see a remote's infrared light through a phone camera. | Infrared is used in remotes, night vision, and heat sensors.
sub-ghz | - | - | Sub-GHz means radio signals below one gigahertz, used by things like garage doors and car keys. | Sub-GHz signals travel farther than WiFi signals. | Sub-GHz radio is used for remotes, sensors, and long range links.
nfc | - | - | NFC is a short range wireless technology for tapping cards and phones together. | NFC only works when things are a few centimeters apart. | NFC is used for tap to pay, key cards, and sharing info.
rfid | - | - | RFID is a technology that uses radio waves to read tags, like ID cards and store tags. | Some RFID tags have no battery at all. | RFID is used for key cards, pet microchips, and tracking items.
3d printer | 3d printers | a | A 3D printer is a machine that builds objects layer by layer from plastic. | 3D printers can make toys, parts, and even houses. | 3D printers are used to make parts and prototypes.
relay | relays | a | A relay is a switch that is turned on and off by electricity. | Relays let a tiny chip control a big motor or light. | Relays are used to switch big loads with a small signal.
voltage regulator | voltage regulators | a | A voltage regulator is a part that keeps the voltage steady. | My board has a regulator that makes 3.3 volts from USB power. | Voltage regulators are used to power chips safely.
wire | wires | a | A wire is a thin metal strand that carries electricity. | Most wires are made of copper. | Wires are used to connect parts in a circuit.
switch | switches | a | A switch is a part that turns a circuit on or off. | A light switch opens and closes a circuit. | Switches are used to turn things on and off.
button | buttons | a | A button is something you press to make a device do something. | Many buttons only connect the circuit while you press them. | Buttons are used to control devices.
speaker | speakers | a | A speaker is a device that turns electricity into sound. | Speakers use a magnet to move a cone back and forth. | Speakers are used to play music and sounds.
microphone | microphones | a | A microphone is a device that turns sound into electricity. | Your phone has tiny microphones inside. | Microphones are used to record and send voices.
buzzer | buzzers | a | A buzzer is a small part that makes a beeping sound. | Many alarms use a buzzer. | Buzzers are used for beeps and alarms.
potentiometer | potentiometers | a | A potentiometer is a knob that changes resistance when you turn it. | Volume knobs are often potentiometers. | Potentiometers are used as knobs to control things.
i2c | - | - | I2C is a simple way for chips to talk using two wires. | Each I2C device has its own address. | I2C is used to connect sensors and screens.
spi | - | - | SPI is a fast way for chips to talk using a few wires and a clock. | SPI is often faster than I2C. | SPI is used for screens, memory, and radios.
uart | - | - | UART is a simple serial link where chips send data one bit at a time. | I talk to you through a serial connection. | UART is used for serial communication and debugging.
laser | lasers | a | A laser is a device that makes a very narrow, bright beam of light. | Never point a laser at someone's eyes. | Lasers are used for pointers, barcode scanners, and cutting.
"""

EXTRA_UNKNOWN = """abacus catapult gondola origami sombrero tiara yacht sphinx trebuchet monocle kimono lantern
chandelier parachute bonsai cymbal didgeridoo escalator fountain hammock jigsaw kettle lasso mosaic obelisk
pagoda quilt raft saddle tambourine unicycle vase whistle ziggurat aardvark ibex jackal kookaburra lamprey
mandrill numbat ocelot quail tarsier vole wallaby wildebeest zebu dugong gibbon macaw magpie nightingale
quetzal capybara coyote dodo emu gorgonzola hyacinth iceberg javelin karate lighthouse marimba nectarine
oboe papaya quinoa radish scarecrow turnip ukulele velvet walnut yeti zipline""".split()

LOOKALIKE_PREFIX = ["hot", "sun", "sea", "fire", "moon", "star", "rain", "snow", "house", "ice", "sand", "mud",
                    "water", "rock", "sword", "bull", "jelly", "gold", "silver", "tree", "night", "day", "sky",
                    "box", "pan", "cup", "egg", "leaf", "salt", "milk"]


def _split(line, n):
    parts = [p.strip() for p in line.split("|")]
    assert len(parts) == n, (len(parts), line[:60])
    return parts


def parse_struct():
    out = {}
    for line in ANIMAL_STRUCT_TEXT.strip().splitlines():
        n, cls, size, legs, ab, foods, diet = _split(line, 7)
        out[n] = dict(cls=cls, size=int(size), legs=int(legs), abil=ab.split(), foods=[f.strip() for f in foods.split(",") if f.strip()], diet=diet)
    return out


def parse_new_animals():
    kb, attrs, struct = [], {}, {}
    for line in NEW_ANIMALS_TEXT.strip().splitlines():
        (n, pl, art, ans, more, eat, live, likes, cls, size, legs, ab, foods, diet) = _split(line, 14)
        kb.append(dict(name=n, plural=None if pl == "-" else pl, article=None if art == "-" else art, answer=ans, more=more))
        attrs[n] = {"eat": eat, "live": live, "likes": likes}
        struct[n] = dict(cls=cls, size=int(size), legs=int(legs), abil=ab.split(), foods=[f.strip() for f in foods.split(",") if f.strip()], diet=diet)
    return kb, attrs, struct


def parse_new_topics():
    kb, used = [], {}
    for line in NEW_TOPICS_TEXT.strip().splitlines():
        n, pl, art, ans, more, u = _split(line, 6)
        kb.append(dict(name=n, plural=None if pl == "-" else pl, article=None if art == "-" else art, answer=ans, more=more))
        if u != "-":
            used[n] = u
    return kb, used
