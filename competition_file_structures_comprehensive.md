# Competition File Structure Summary

Detailed view of each competition's data directory. The grader mounts these at `./data` (read-only). Compressed assets remain compressed in `./data`; decompress them into the working directory before use.

## 3d-object-detection-for-autonomous-vehicles
Tables:
- `sample_submission.csv` — 4537 rows; first lines:
  ```
  Id,PredictionString
  5796b008cea965d2ff1d8f653d93b5d29aed64c22d6b89afd9b203897c20a07d,
  6ae782254574cee52863efb671a6208dd0f31b45fa5f1e5912e797eb5e4888f7,
  ```
- `train.csv` — 18145 rows; first lines:
  ```
  Id,PredictionString
  db8b47bd4ebdf3b3fb21598bb41bd8853d12f8d2ef25ce76edd4af4d04e49341,2680.2830359778527 698.1969292852777 -18.04776692365821 2.064 5.488 2.053 2.6041643845397946 car 2691.997461646401 660.8016536569899 -1…
  edf37c1fb1024ba0c1f53ebbf10b6797f781199a9f0e4e25274df2448966d929,1208.642684768659 1585.1812946970927 -23.56236391728106 1.635 4.339 1.515 -0.5649508769816922 car 1156.4066827993538 1630.2869876546688…
  ```
Folders:
- `test_data/` — 11 files, 0 subfolders; examples: log.json, sensor.json, sample.json
- `test_images/` — 31752 files, 0 subfolders; examples: host-a011_cam1_1236093974934517006.jpeg, host-a011_cam6_1234639315651145006.jpeg, host-a011_cam2_1235866720517605006.jpeg
- `test_lidar/` — 5544 files, 0 subfolders; examples: host-a004_lidar1_1233014353901256606.bin, host-a015_lidar1_1233957278701251246.bin, host-a101_lidar0_1241561169502447046.bin
- `test_maps/` — 1 files, 0 subfolders; examples: map_raster_palo_alto.png
- `train_data/` — 13 files, 0 subfolders; examples: log.json, sensor.json, instance.json
- `train_images/` — 127005 files, 0 subfolders; examples: host-a009_cam1_1236014664834319006.jpeg, host-a004_cam6_1235947081550948006.jpeg, host-a007_cam6_1234551932350905006.jpeg
- `train_lidar/` — 25200 files, 0 subfolders; examples: host-a102_lidar1_1242510604902197254.bin, host-a004_lidar1_1232833312701287486.bin, host-a009_lidar1_1236015619801163246.bin
- `train_maps/` — 1 files, 0 subfolders; examples: map_raster_palo_alto.png

## AI4Code
Tables:
- `sample_submission.csv` — 20001 rows; first lines:
  ```
  id,cell_order
  00015c83e2717b,c417225b 51e3cd89 2600b4eb 75b65993 cf195f8b 25699d02 de148b56 9901472c 10377ef8 1f462e2f fceeb3e6 2af2a41a 91e68f13 9216a113 63753f10 d5aee1e4 dc8a39a5 3d0a28c2 0eea9701 a6f8f9f1 7223c…
  0001bdd4021779,3fdc37be 073782ca 8ea7263c 80543cd8 38310c80 073e27e5 015d52a4 ad7679ef 07c52510 0a1a7a39 0bcd3fef 7fde4f04 58bf360b
  ```
- `train_ancestors.csv` — 119257 rows; first lines:
  ```
  id,ancestor_id,parent_id
  d87cd768d60617,edd9d4e9,
  22931fba2feaba,f5d11468,
  ```
- `train_orders.csv` — 119257 rows; first lines:
  ```
  id,cell_order
  00001756c60be8,1862f0a6 448eb224 2a9e43d6 7e2f170a 038b763d 77e56113 2eefe0ef 1ae087ab 0beab1cd 8ffe0b25 9a78ab76 0d136e08 8a4c95d1 23705731 ebe125d5 aaad8355 d9dced8b 21616367 86497fe1 c3ce0945 e2c8e…
  0001daf4c2c76d,97266564 a898e555 86605076 76cc2642 ef279279 df6c939f 2476da96 00f87d0a ae93e8e6 58aadb1d d20b0094 986fd4f1 b4ff1015 9b761026 6f271c86 97c3f99b 2451daed cfa510c5 374a5179 df5f7c1f 27060…
  ```
Folders:
- `test/` — 20000 files, 0 subfolders; examples: c9c079866d726d.json, 09ebcca470746e.json, 90c7986669602a.json
- `train/` — 119256 files, 0 subfolders; examples: 924d94f41cf200.json, b5469d43c786df.json, 95eef4b4f3be4e.json

## aerial-cactus-identification
Tables:
- `sample_submission.csv` — 3326 rows; first lines:
  ```
  id,has_cactus
  09034a34de0e2015a8a28dfe18f423f6.jpg,0.5
  134f04305c795d6d202502c2ce3578f3.jpg,0.5
  ```
- `train.csv` — 14176 rows; first lines:
  ```
  id,has_cactus
  2de8f189f1dce439766637e75df0ee27.jpg,1
  36704d250f236238e7f996812c48235d.jpg,1
  ```
Compressed artifacts:
- `test.zip` [compressed] (entries: 3325) — first entries: 498701365baa67a893be58ec3b5e65b1.jpg, 5e8409129d57a3723fa7f389fc0cfa06.jpg, d13cd6591afc04a0efb6fcb9f63bf8df.jpg, 85973aae10bd19e13a453a52e1a6518d.jpg, 3b9e951230e3fc7f2c6322cf4ae4a55e.jpg
- `train.zip` [compressed] (entries: 14175) — first entries: 1bdb98f00f06b958a1d07ba0165a435b.jpg, 63d42901f6156fca193e129ec00b7d2d.jpg, 3fd96cf1aa65044723eb774e8262d5be.jpg, 1e18e941f7badfd9d3b3905f62317a96.jpg, 81cf14f139a607dc4678a2d4430dab03.jpg

## alaska2-image-steganalysis
Tables:
- `sample_submission.csv` — 5001 rows; first lines:
  ```
  Id,Label
  0001.jpg,0
  0002.jpg,0
  ```
Folders:
- `Cover/` — 70000 files, 0 subfolders; examples: 38827.jpg, 04123.jpg, 51777.jpg
- `JMiPOD/` — 70000 files, 0 subfolders; examples: 38827.jpg, 04123.jpg, 51777.jpg
- `JUNIWARD/` — 70000 files, 0 subfolders; examples: 38827.jpg, 04123.jpg, 51777.jpg
- `Test/` — 5000 files, 0 subfolders; examples: 3191.jpg, 2057.jpg, 4856.jpg
- `UERD/` — 70000 files, 0 subfolders; examples: 38827.jpg, 04123.jpg, 51777.jpg

## aptos2019-blindness-detection
Tables:
- `sample_submission.csv` — 368 rows; first lines:
  ```
  id_code,diagnosis
  b460ca9fa26f,0
  6cee2e148520,0
  ```
- `test.csv` — 368 rows; first lines:
  ```
  id_code
  b460ca9fa26f
  6cee2e148520
  ```
- `train.csv` — 3296 rows; first lines:
  ```
  id_code,diagnosis
  2a2274bcb00a,0
  eda29a9d78f3,0
  ```
Folders:
- `test_images/` — 367 files, 0 subfolders; examples: a85cda5f725d.png, a26f50218b84.png, 77baa08a1345.png
- `train_images/` — 3295 files, 0 subfolders; examples: 1dfbede13143.png, 4e82c3c8d31f.png, 932181b93b2f.png

## billion-word-imputation
Tables:
- `test_v2.txt (inside test_v2.txt.zip)` — 302645 rows; first lines:
  ```
  "id","sentence"
  0,"Ditto her cut-offs ."
  1,"The game that Brosnan lent his voice to ."
  ```
- `train_v2.txt (inside train_v2.txt.zip)` — 29998384 rows; first lines:
  ```
  The U.S. Centers for Disease Control and Prevention initially advised school systems to close if outbreaks occurred , then reversed itself , saying the apparent mildness of the virus meant most school…
  When Ms. Winfrey invited Suzanne Somers to share her controversial views about bio-identical hormone treatment on her syndicated show in 2009 , it won Ms. Winfrey a rare dollop of unflattering press ,…
  Elk calling -- a skill that hunters perfected long ago to lure game with the promise of a little romance -- is now its own sport .
  ```
Compressed artifacts:
- `test_v2.txt.zip` [compressed] (entries: 1) — first entries: test_v2.txt
- `train_v2.txt.zip` [compressed] (entries: 1) — first entries: train_v2.txt

## bms-molecular-translation
Tables:
- `extra_approved_InChIs.csv` — 9998712 rows; first lines:
  ```
  InChI
  InChI=1S/C13H10Cl4O4/c1-20-13(21-2)11(16)5-6-8(19)4-3(7(5)18)9(11,14)10(4,15)12(6,13)17/h3-6H,1-2H3/t3-,4+,5-,6-,9+,10+,11+,12-/m0/s1
  InChI=1S/C23H32O6Si/c1-20(2)25-15-19(27-20)22(29-30(5,6)7)13-8-9-17(24)23-16(12-14-22)10-11-18(23)26-21(3,4)28-23/h10,17-19,24H,11,13,15H2,1-7H3/t17-,18-,19+,22-,23-/m1/s1
  ```
- `sample_submission.csv` — 484839 rows; first lines:
  ```
  image_id,InChI
  920b92cd823f,InChI=1S/H2O/h1H2
  fb2634d1976d,InChI=1S/H2O/h1H2
  ```
- `train_labels.csv` — 1939349 rows; first lines:
  ```
  image_id,InChI
  5af83da44ed4,InChI=1S/C25H26F5N/c1-2-3-4-5-17-6-8-18(9-7-17)19-10-11-24(31-16-19)20-14-22(26)21(23(27)15-20)12-13-25(28,29)30/h10-11,14-18H,2-9H2,1H3
  50d54d1589b8,InChI=1S/C21H16ClNO5/c22-16-8-20-19(27-10-28-20)6-12(16)9-23-17-4-2-13(24)7-15(17)14-3-1-11(21(25)26)5-18(14)23/h1,3,5-6,8H,2,4,7,9-10H2,(H,25,26)
  ```
Folders:
- `test/` — 0 files, 16 subfolders; examples: 8/8, 5/8, e/8
- `train/` — 0 files, 16 subfolders; examples: 8/8, 5/8, e/8

## cassava-leaf-disease-classification
Tables:
- `label_num_to_disease_map.json` — rows: n/a; first lines:
  ```
  ```
- `sample_submission.csv` — 2677 rows; first lines:
  ```
  image_id,label
  1234294272.jpg,4
  1234332763.jpg,4
  ```
- `train.csv` — 18722 rows; first lines:
  ```
  image_id,label
  1000015157.jpg,0
  1000201771.jpg,3
  ```
Folders:
- `test_images/` — 2676 files, 0 subfolders; examples: 1378311298.jpg, 2512244783.jpg, 2614438244.jpg
- `test_tfrecords/` — 2 files, 0 subfolders; examples: ld_test00-1338.tfrec, ld_test01-1338.tfrec
- `train_images/` — 18721 files, 0 subfolders; examples: 3899862618.jpg, 228290866.jpg, 953218056.jpg
- `train_tfrecords/` — 14 files, 0 subfolders; examples: ld_train02-1338.tfrec, ld_train00-1338.tfrec, ld_train07-1338.tfrec

## cdiscount-image-classification-challenge
Tables:
- `category_names.csv` — 5271 rows; first lines:
  ```
  category_id,category_level1,category_level2,category_level3
  1000021794,ABONNEMENT / SERVICES,CARTE PREPAYEE,CARTE PREPAYEE MULTIMEDIA
  1000012764,AMENAGEMENT URBAIN - VOIRIE,AMENAGEMENT URBAIN,ABRI FUMEUR
  ```
- `sample_submission.csv` — 706991 rows; first lines:
  ```
  _id,category_id
  6,1000010653
  7,1000010653
  ```

## chaii-hindi-and-tamil-question-answering
Tables:
- `sample_submission.csv` — 113 rows; first lines:
  ```
  id,PredictionString
  be799d365,dummy text
  26f356026,dummy text
  ```
- `test.csv` — 7173 rows; first lines:
  ```
  id,context,question,language
  be799d365,एशियन पेंट्स लिमिटेड एक भारतीय बहुराष्ट्रीय कम्पनी है जिसका मुख्यालय मुंबई, महाराष्ट्र में है।[2] ये कम्पनी, रंग, घर की सजावट, फिटिंग से संबंधित उत्पादों और संबंधित सेवाएं प्रदान करने, निर्म…
  26f356026,स्वामी निगमानन्द परमहंस (18 अगस्त 1880 - 29 नवम्बर 1935) भारत के एक महान सन्यासी ब सदगुरु थे।[1] उनके शिश्य लोगं उन्हें आदरपूर्वक श्री श्री ठाकुर बुलाते हैं। ऐसा माना जाता है की स्वामी निगमा…
  ```
- `train.csv` — 67723 rows; first lines:
  ```
  id,context,question,answer_text,answer_start,language
  6bb0c472d,சிங்கம் என்பது பாலூட்டி வகையைச் சேர்ந்த ஒரு காட்டு விலங்கு ஆகும். இவ்விலங்கு ஊன் உண்ணும் விலங்கு வகையைச் சேர்ந்தது. தமிழில் ஆண் சிங்கத்தை அரிமா என்றும், பெண் சிங்கத்தை சிம்மம் என்றும் கூறுவத…
  34846a420,சென்னை (Chennai) தமிழ்நாட்டின் தலைநகரமும் இந்தியாவின் நான்காவது பெரிய நகரமும் ஆகும். 1996 ஆம் ஆண்டுக்கு முன்னர் இந்நகரம் மெட்ராஸ் (Madras) என்று அழைக்கப்பட்டு வந்தது. சென்னை, வங்காள விரிகுடா…
  ```

## champs-scalar-coupling
Tables:
- `dipole_moments.csv` — 76511 rows; first lines:
  ```
  molecule_name,X,Y,Z
  dsgdb9nsd_000001,0.0,0.0,0.0
  dsgdb9nsd_000002,-0.0002,0.0,1.6256
  ```
- `magnetic_shielding_tensors.csv` — 1379965 rows; first lines:
  ```
  molecule_name,atom_index,XX,YX,ZX,XY,YY,ZY,XZ,YZ,ZZ
  dsgdb9nsd_000001,0,195.3147,0.0,-0.0001,0.0,195.3171,0.0007,-0.0001,0.0007,195.3169
  dsgdb9nsd_000001,1,31.341,-1.2317,4.0544,-1.2317,28.9546,-1.7173,4.0546,-1.7173,34.0861
  ```
- `mulliken_charges.csv` — 1379965 rows; first lines:
  ```
  molecule_name,atom_index,mulliken_charge
  dsgdb9nsd_000001,0,-0.5356890000000001
  dsgdb9nsd_000001,1,0.133921
  ```
- `potential_energy.csv` — 76511 rows; first lines:
  ```
  molecule_name,potential_energy
  dsgdb9nsd_000001,-40.5236795
  dsgdb9nsd_000002,-56.5602457
  ```
- `sample_submission.csv` — 467814 rows; first lines:
  ```
  id,scalar_coupling_constant
  2324604,0
  2324605,0
  ```
- `scalar_coupling_contributions.csv` — 4191264 rows; first lines:
  ```
  molecule_name,atom_index_0,atom_index_1,type,fc,sd,pso,dso
  dsgdb9nsd_000001,1,0,1JHC,83.0224,0.254579,1.25862,0.27201
  dsgdb9nsd_000001,1,2,2JHH,-11.0347,0.352978,2.85839,-3.4336
  ```
- `structures.csv` — 1379965 rows; first lines:
  ```
  molecule_name,atom_index,atom,x,y,z
  dsgdb9nsd_000001,0,C,-0.012698135900000001,1.0858041578,0.008000995799999999
  dsgdb9nsd_000001,1,H,0.002150416,-0.0060313176,0.0019761204
  ```
- `test.csv` — 467814 rows; first lines:
  ```
  id,molecule_name,atom_index_0,atom_index_1,type
  2324604,dsgdb9nsd_071451,9,0,1JHC
  2324605,dsgdb9nsd_071451,9,1,2JHC
  ```
- `train.csv` — 4191264 rows; first lines:
  ```
  id,molecule_name,atom_index_0,atom_index_1,type,scalar_coupling_constant
  3872080,dsgdb9nsd_109986,9,0,1JHC,95.47
  3872081,dsgdb9nsd_109986,9,2,3JHC,1.47412
  ```
Folders:
- `structures/` — 76510 files, 0 subfolders; examples: dsgdb9nsd_059882.xyz, dsgdb9nsd_012141.xyz, dsgdb9nsd_074725.xyz

## denoising-dirty-documents
Tables:
- `sampleSubmission.csv` — 5789881 rows; first lines:
  ```
  id,value
  110_1_1,1
  110_1_2,1
  ```
Folders:
- `test/` — 29 files, 0 subfolders; examples: 110.png, 186.png, 162.png
- `train/` — 115 files, 0 subfolders; examples: 167.png, 69.png, 171.png
- `train_cleaned/` — 115 files, 0 subfolders; examples: 167.png, 69.png, 171.png

## detecting-insults-in-social-commentary
Tables:
- `sample_submission_null.csv` — 2648 rows; first lines:
  ```
  Insult,Date,Comment
  0,,"THE DRUDGE REPORT\\n\\n\\n\\nYou won't see this story on foxfag forum because they suck bIacks and gay 0bama all the way to the crack.\\n\\n\\n\\n\\n\\n\\n\\nOn Tuesday Rep. Darrell Issa, chairman…
  0,20120618222256Z,"@ian21\xa0"Roger Clemens is the fucking man, and never did any fucking steroids because he is fucking awesome. Did you all misremember Roger's incredibleness?" - Roger Clemens"
  ```
- `test.csv` — 2648 rows; first lines:
  ```
  Date,Comment
  ,"THE DRUDGE REPORT\\n\\n\\n\\nYou won't see this story on foxfag forum because they suck bIacks and gay 0bama all the way to the crack.\\n\\n\\n\\n\\n\\n\\n\\nOn Tuesday Rep. Darrell Issa, chairman o…
  20120618222256Z,"@ian21\xa0"Roger Clemens is the fucking man, and never did any fucking steroids because he is fucking awesome. Did you all misremember Roger's incredibleness?" - Roger Clemens"
  ```
- `train.csv` — 3948 rows; first lines:
  ```
  Insult,Date,Comment
  1,20120618192155Z,"You fuck your dad."
  0,20120528192215Z,"i really don't understand your point.\xa0 It seems that you are mixing apples and oranges."
  ```

## dog-breed-identification
Tables:
- `labels.csv` — 9200 rows; first lines:
  ```
  id,breed
  8406d837b2d7fac1c3cd621abb4c4f9e,west_highland_white_terrier
  e270622b5ffec8294d7e7628c4ff6c1e,brittany_spaniel
  ```
- `sample_submission.csv` — 1024 rows; first lines:
  ```
  id,affenpinscher,afghan_hound,african_hunting_dog,airedale,american_staffordshire_terrier,appenzeller,australian_terrier,basenji,basset,beagle,bedlington_terrier,bernese_mountain_dog,black-and-tan_coo…
  9f68d045a396679a778eb54c5ed29038,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333…
  f375e6363bc21dcd3cb65637c7855e9c,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333,0.008333333333333333…
  ```
Folders:
- `test/` — 1023 files, 0 subfolders; examples: fa24ae09f6c25172009016b9dbec322d.jpg, c05756fc992ab5863853dafe9cf50675.jpg, 1c80cbd184334b339e5eba8aaa6ae929.jpg
- `train/` — 9199 files, 0 subfolders; examples: 5cdd18e46b1877eabfa82bb4c40af15b.jpg, 34455076d8d7c9e83eed6cfde1e29670.jpg, e60889840323eb4be2ff9498c79c1409.jpg

## dogs-vs-cats-redux-kernels-edition
Tables:
- `sample_submission.csv` — 2501 rows; first lines:
  ```
  id,label
  1,0.5
  2,0.5
  ```
Compressed artifacts:
- `test.zip` [compressed] (entries: 2500) — first entries: 2057.jpg, 357.jpg, 2030.jpg, 1062.jpg, 1261.jpg
- `train.zip` [compressed] (entries: 22500) — first entries: dog.9174.jpg, dog.1872.jpg, dog.8892.jpg, dog.3581.jpg, dog.8694.jpg
Folders:
- `test/` — 2500 files, 0 subfolders; examples: 2057.jpg, 357.jpg, 2030.jpg
- `train/` — 22500 files, 0 subfolders; examples: dog.9174.jpg, dog.1872.jpg, dog.8892.jpg

## facebook-recruiting-iii-keyword-extraction
Tables:
- `sample_submission.csv` — 14567652 rows; first lines:
  ```
  Id,Title,Body,Tags
  860708,How can I write a group of reference briefly? ([1, 2, 3, 4, 5] change to [1-5] but show the all refer on reference),<blockquote>
  <p><strong>Possible Duplicate:</strong><br>
  <a href="http://…
  4774265,Applying default umask on various platforms,<p>What is the best practice to apply default user <code>umask</code> value on various platforms in <code>C</code>? I'm writing a file packaging lib…
  ```
- `test.csv` — 14567652 rows; first lines:
  ```
  Id,Title,Body
  860708,How can I write a group of reference briefly? ([1, 2, 3, 4, 5] change to [1-5] but show the all refer on reference),<blockquote>
  <p><strong>Possible Duplicate:</strong><br>
  <a href="http://…
  4774265,Applying default umask on various platforms,<p>What is the best practice to apply default user <code>umask</code> value on various platforms in <code>C</code>? I'm writing a file packaging lib…
  ```
- `train.csv` — 130879606 rows; first lines:
  ```
  Id,Title,Body,Tags
  818237,mysql + issues with JOIN query,<p>Ok folks, im sorry to ask about this since ive seen a couple of mysql JOIN examples but i seem to be unable to get it to work.</p>

<p>"sales"</p>

<pre><code>…
  5980619,Same UITableViewDataSource for two UITableView,<p>I'm developing an iPhone application with latest SDK and XCode 4.5.2.</p>

<p>On a ViewController I have two <code>UITableView</code>. Both us…
  ```

## freesound-audio-tagging-2019
Tables:
- `sample_submission.csv` — 3362 rows; first lines:
  ```
  fname,Accelerating_and_revving_and_vroom,Accordion,Acoustic_guitar,Applause,Bark,Bass_drum,Bass_guitar,Bathtub_(filling_or_washing),Bicycle_bell,Burping_and_eructation,Bus,Buzz,Car_passing_by,Cheering…
  4260ebea.wav,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  426eb1e0.wav,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  ```
- `train_curated.csv` — 4971 rows; first lines:
  ```
  fname,labels
  0006ae4e.wav,Bark
  0019ef41.wav,Raindrop
  ```
- `train_noisy.csv` — 19816 rows; first lines:
  ```
  fname,labels
  00097e21.wav,Bathtub_(filling_or_washing)
  000b6cfb.wav,Motorcycle
  ```
Compressed artifacts:
- `test.zip` [compressed] (entries: 3361) — first entries: 66b82f03.wav, e667e7ad.wav, 488b78b0.wav, 8206c573.wav, f150ff14.wav
- `train_curated.zip` [compressed] (entries: 4970) — first entries: c1b84d6f.wav, 37acc887.wav, 8d1fb22b.wav, fd621ec3.wav, b2196421.wav
- `train_noisy.zip` [compressed] (entries: 19815) — first entries: 6dd81c5a.wav, 8673f1a1.wav, 0eb824eb.wav, f97e8551.wav, 84ca96ab.wav

## google-quest-challenge
Tables:
- `sample_submission.csv` — 609 rows; first lines:
  ```
  qa_id,question_asker_intent_understanding,question_body_critical,question_conversational,question_expect_short_answer,question_fact_seeking,question_has_commonly_accepted_answer,question_interestingne…
  6516,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
  6168,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.0016474464579901153,0.00164744645799011…
  ```
- `test.csv` — 19551 rows; first lines:
  ```
  qa_id,question_title,question_body,question_user_name,question_user_page,answer,answer_user_name,answer_user_page,url,category,host
  6516,"Hirable" or "hireable",What is the correct adjective form of the word hire? I have seen references to both hireable and hirable. 

I checked using Google's Ngram viewer book search and it appear…
  6168,Setting text of UITextField from caller view,I have a barcode scanner on one view, and after the user has scanned the barcode, the app takes them to another view (BoilerDetails) where the barcode…
  ```
- `train.csv` — 159837 rows; first lines:
  ```
  qa_id,question_title,question_body,question_user_name,question_user_page,answer,answer_user_name,answer_user_page,url,category,host,question_asker_intent_understanding,question_body_critical,question_…
  9622,Which parts of fresh Fenugreek am I supposed to throw off before attempting to dry them out completely?,The fresh Fenugreek which I bought contains:
- long stems
- green leaves
- yellow leaves   …
  3515,Is decoherence even possible in anti de Sitter space?,Is decoherence even possible in anti de Sitter space? The spatial conformal boundary acts as a repulsive wall, thus turning anti de Sitter sp…
  ```

## google-research-identify-contrails-reduce-global-warming
Tables:
- `sample_submission.csv` — 1857 rows; first lines:
  ```
  record_id,encoded_pixels,height,width
  4265087624835862793,-,256,256
  5940742775168609422,-,256,256
  ```
- `train_metadata.json` — rows: n/a; first lines:
  ```
  ```
- `validation_metadata.json` — rows: n/a; first lines:
  ```
  ```
Folders:
- `test/` — 0 files, 1856 subfolders; examples: 9035554291400142136/band_09.npy, 988163370871338338/band_09.npy, 3761056165862978238/band_09.npy
- `train/` — 0 files, 18673 subfolders; examples: 2434935274349365772/band_09.npy, 1523353774599390385/band_09.npy, 3993468539889351042/band_09.npy
- `validation/` — 0 files, 1856 subfolders; examples: 6968129562736251517/band_09.npy, 5644499949408336412/band_09.npy, 1197588539102419511/band_09.npy

## h-and-m-personalized-fashion-recommendations
Tables:
- `articles.csv` — 105543 rows; first lines:
  ```
  article_id,product_code,prod_name,product_type_no,product_type_name,product_group_name,graphical_appearance_no,graphical_appearance_name,colour_group_code,colour_group_name,perceived_colour_value_id,p…
  0108775015,0108775,Strap top,253,Vest top,Garment Upper body,1010016,Solid,09,Black,4,Dark,5,Black,1676,Jersey Basic,A,Ladieswear,1,Ladieswear,16,Womens Everyday Basics,1002,Jersey Basic,Jersey top wi…
  0108775044,0108775,Strap top,253,Vest top,Garment Upper body,1010016,Solid,10,White,3,Light,9,White,1676,Jersey Basic,A,Ladieswear,1,Ladieswear,16,Womens Everyday Basics,1002,Jersey Basic,Jersey top w…
  ```
- `customers.csv` — 1371981 rows; first lines:
  ```
  customer_id,FN,Active,club_member_status,fashion_news_frequency,age,postal_code
  00000dbacae5abe5e23885899a1fa44253a17956c6d1c3d25f88aa139fdfc657,,,ACTIVE,NONE,49,52043ee2162cf5aa7ee79974281641c6f11a68d276429a91f8ca0d4b6efa8100
  0000423b00ade91418cceaf3b26c6af3dd342b51fd051eec9c12fb36984420fa,,,ACTIVE,NONE,25,2973abc54daa8a5f8ccfe9362140c63247c5eee03f1d93f4c830291c32bc3057
  ```
- `sample_submission.csv` — 1371981 rows; first lines:
  ```
  customer_id,prediction
  00000dbacae5abe5e23885899a1fa44253a17956c6d1c3d25f88aa139fdfc657,0706016001 0706016002 0372860001 0610776002 0759871002 0464297007 0372860002 0610776001 0399223001 0706016003 0720125001 0156231001
  0000423b00ade91418cceaf3b26c6af3dd342b51fd051eec9c12fb36984420fa,0706016001 0706016002 0372860001 0610776002 0759871002 0464297007 0372860002 0610776001 0399223001 0706016003 0720125001 0156231001
  ```
- `transactions_train.csv` — 31521961 rows; first lines:
  ```
  t_dat,customer_id,article_id,price,sales_channel_id
  2018-09-20,000058a12d5b43e67d225668fa1f8d618c13dc232df0cad8ffe7ad4a1091e318,663713001,0.050830508474576264,2
  2018-09-20,000058a12d5b43e67d225668fa1f8d618c13dc232df0cad8ffe7ad4a1091e318,541518023,0.03049152542372881,2
  ```
Folders:
- `images/` — 0 files, 86 subfolders; examples: 049/0498480001.jpg, 046/0466948031.jpg, 011/0111565001.jpg

## herbarium-2020-fgvc7
Tables:
- `sample_submission.csv` — 219125 rows; first lines:
  ```
  Id,Predicted
  0,0
  1,0
  ```
Folders:
- `nybg2020/` — 0 files, 2 subfolders; examples: train/images, test/images

## herbarium-2021-fgvc8
Tables:
- `sample_submission.csv` — 477807 rows; first lines:
  ```
  Id,Predicted
  0,0
  1,0
  ```
Folders:
- `test/` — 1 files, 1 subfolders; examples: metadata.json, images/440
- `train/` — 1 files, 1 subfolders; examples: metadata.json, images/440

## herbarium-2022-fgvc9
Tables:
- `sample_submission.csv` — 174053 rows; first lines:
  ```
  Id,Predicted
  0,42
  1,42
  ```
- `test_metadata.json` — rows: n/a; first lines:
  ```
  [
      {
          "file_name": "000/test-000000.jpg",
  ```
- `train_metadata.json` — rows: n/a; first lines:
  ```
  {
      "annotations": [
          {
  ```
Folders:
- `test_images/` — 0 files, 175 subfolders; examples: 049/test-049059.jpg, 001/test-001048.jpg, 046/test-046495.jpg
- `train_images/` — 0 files, 156 subfolders; examples: 049/49, 001/49, 046/49

## histopathologic-cancer-detection
Tables:
- `sample_submission.csv` — 45562 rows; first lines:
  ```
  id,label
  acfe80838488fae3c89bd21ade75be5c34e66be7,0
  a1991e73a9b676faddd2bd47c39754b14d1eb923,0
  ```
- `train_labels.csv` — 174465 rows; first lines:
  ```
  id,label
  f38a6374c348f90b587e046aac6079959adf3835,0
  c18f2d887b7ae4f6742ee445113fa1aef383ed77,1
  ```
Folders:
- `test/` — 45561 files, 0 subfolders; examples: 9f355f394e8032ab74e6c01cff46f4014ba0799a.tif, 7d67c2d809dc817f866f1d14bab96884fde6e6a9.tif, d1e31614a87de1f21dc69d3a21153cdbea906c66.tif
- `train/` — 174464 files, 0 subfolders; examples: 440101b10ccc3b62064670d38fb78e318bafaffe.tif, 69d572155eff030e3252324c3289debb4cb83437.tif, 3e31e8f3378085700f16b8ea7fa5fe3b9bb1914d.tif

## hms-harmful-brain-activity-classification
Tables:
- `sample_submission.csv` — 9851 rows; first lines:
  ```
  eeg_id,seizure_vote,lpd_vote,gpd_vote,lrda_vote,grda_vote,other_vote
  2578018731,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666
  2578018731,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666
  ```
- `test.csv` — 9851 rows; first lines:
  ```
  spectrogram_id,eeg_id,patient_id
  2207717,2578018731,34153
  2207717,2578018731,34153
  ```
- `train.csv` — 96951 rows; first lines:
  ```
  eeg_id,eeg_sub_id,eeg_label_offset_seconds,spectrogram_id,spectrogram_sub_id,spectrogram_label_offset_seconds,label_id,patient_id,expert_consensus,seizure_vote,lpd_vote,gpd_vote,lrda_vote,grda_vote,ot…
  1628180742,0,0.0,353733,0,0.0,127492639,42516,Seizure,3,0,0,0,0,0
  1628180742,1,6.0,353733,1,6.0,3887563113,42516,Seizure,3,0,0,0,0,0
  ```
Folders:
- `example_figures/` — 20 files, 0 subfolders; examples: Sample20.pdf, Sample05.pdf, Sample03.pdf
- `test_eegs/` — 1693 files, 0 subfolders; examples: 485584929.parquet, 490643850.parquet, 413361968.parquet
- `test_spectrograms/` — 1114 files, 0 subfolders; examples: 1900830830.parquet, 2024255395.parquet, 709469540.parquet
- `train_eegs/` — 15396 files, 0 subfolders; examples: 868415395.parquet, 2138881026.parquet, 1406486249.parquet
- `train_spectrograms/` — 10024 files, 0 subfolders; examples: 1440635038.parquet, 180285509.parquet, 445262921.parquet

## hotel-id-2021-fgvc8
Tables:
- `sample_submission.csv` — 9757 rows; first lines:
  ```
  image,hotel_id
  f1608c9f17fb6920.jpg,36363 53586 18807 64314 60181
  c6c63939c67931e1.jpg,36363 53586 18807 64314 60181
  ```
- `train.csv` — 87799 rows; first lines:
  ```
  image,chain,hotel_id,timestamp
  d29287f52c2a871f.jpg,5,22408,2018-04-16 17:01:49
  e9d067c249e4c2f9.jpg,70,2324,2016-07-08 22:26:21
  ```
Folders:
- `test_images/` — 9756 files, 0 subfolders; examples: 83939bb26cb464f4.jpg, 92926d6c6c9e338b.jpg, 95c90ef6e90aed03.jpg
- `train_images/` — 0 files, 88 subfolders; examples: 8/b7b7016a6a694d4a.jpg, 49/c06a1fe5c23d3ec1.jpg, 32/824cf0d3adcaccd6.jpg

## hubmap-kidney-segmentation
Tables:
- `HuBMAP-20-dataset_information.csv` — 16 rows; first lines:
  ```
  image_file,width_pixels,height_pixels,anatomical_structures_segmention_file,glomerulus_segmentation_file,patient_number,race,ethnicity,sex,age,weight_kilograms,height_centimeters,bmi_kg/m^2,laterality…
  afa5e8098.tiff,43780,36800,afa5e8098-anatomical-structure.json,afa5e8098.json,67347,White,Not Hispanic or Latino,Female,58,59.0,160.0,23.0,Right,55,45
  54f2eec69.tiff,22240,30440,54f2eec69-anatomical-structure.json,54f2eec69.json,67548,Black or African American,Not Hispanic or Latino,Male,58,79.9,190.5,22.0,Right,75,25
  ```
- `sample_submission.csv` — 4 rows; first lines:
  ```
  id,predicted
  8242609fa,
  0486052bb,
  ```
- `train.csv` — 13 rows; first lines:
  ```
  ```
Folders:
- `test/` — 10 files, 0 subfolders; examples: 0486052bb.tiff, 0486052bb-anatomical-structure.json, 8242609fa.tiff
- `train/` — 36 files, 0 subfolders; examples: c68fe75ea-anatomical-structure.json, 26dc41664-anatomical-structure.json, c68fe75ea.tiff

## imet-2020-fgvc7
Tables:
- `labels.csv` — 3475 rows; first lines:
  ```
  attribute_id,attribute_name
  0,country::afghanistan
  1,country::alamania
  ```
- `sample_submission.csv` — 21319 rows; first lines:
  ```
  id,attribute_ids
  347c119163f84420f10f7a8126c1b8a2,0 1 2
  98c91458324cba5415c5f5d8ead68328,0 1 2
  ```
- `train.csv` — 120802 rows; first lines:
  ```
  id,attribute_ids
  4d0f6eada4ccb283551bc2f75e2ba588,3077 3187 3418 448 1625 782
  75a9baea36b82e81263716fac427e416,2802 287 370 1419 784
  ```
Folders:
- `test/` — 21318 files, 0 subfolders; examples: ec544c9a89c8a676fa54671d8c1d2238.png, 7583ec05425d65b6884b7a88deb343d8.png, be3c27920342a3aac4de3534af0a99ed.png
- `train/` — 120801 files, 0 subfolders; examples: c6ab2951fde57c51d6d3946c5a486171.png, ba84b16b7af08a262c0a8a6eaed4dc72.png, 61dca2d02d9b39c87292de5a1240bab7.png

## inaturalist-2019-fgvc6
Tables:
- `kaggle_sample_submission.csv` — 32215 rows; first lines:
  ```
  id,predicted
  177388,654
  177102,654
  ```
- `test2019.json` — rows: n/a; first lines:
  ```
  {
      "images": [
          {
  ```
- `train2019.json` — rows: n/a; first lines:
  ```
  {
      "annotations": [
          {
  ```
- `val2019.json` — rows: n/a; first lines:
  ```
  ```
Compressed artifacts:
- `test2019.tar.gz` [compressed] (entries: 32214) — first entries: 66da5cf0439d53aac9a07ce7187c355a.jpg, 48fc66c261bf4608cf54f7e67a238cfa.jpg, 0ee3b42a4815d59702257c71feb5b222.jpg, 57cb7a44397dac9a18762653f0445a45.jpg, 4b260e2e631549996eb3cf3a5ebc7fc2.jpg
- `train_val2019.tar.gz` [compressed] (entries: 232999) — first entries: Insects/49/e978bd17b8f7f5d4a21b3bbcaa5f6081.jpg, Insects/49/75a32b434d19e937cd5ea1f6f2276a90.jpg, Insects/49/5a6e83310857dac2e4b1da940880b449.jpg, Insects/49/44221c55cf63503e356fa1195cdeacc1.jpg, Insects/49/72b0cf1d66a0145c5a4580408b47a57d.jpg

## invasive-species-monitoring
Tables:
- `sample_submission.csv (inside sample_submission.csv.zip)` — 460 rows; first lines:
  ```
  name,invasive
  1960,0.5
  522,0.5
  ```
- `train_labels.csv (inside train_labels.csv.zip)` — 1837 rows; first lines:
  ```
  name,invasive
  1525,1
  2287,1
  ```
Compressed artifacts:
- `sample_submission.csv.zip` [compressed] (entries: 1) — first entries: sample_submission.csv
- `train_labels.csv.zip` [compressed] (entries: 1) — first entries: train_labels.csv

## iwildcam-2019-fgvc6
Tables:
- `sample_submission.csv` — 16878 rows; first lines:
  ```
  ,Id,Category
  0,5998cfa4-23d2-11e8-a6a3-ec086b02610b,0
  4,599fbd89-23d2-11e8-a6a3-ec086b02610b,0
  ```
- `test.csv` — 16878 rows; first lines:
  ```
  date_captured,file_name,frame_num,id,location,rights_holder,seq_id,seq_num_frames,width,height
  2011-05-13 23:43:18,5998cfa4-23d2-11e8-a6a3-ec086b02610b.jpg,1,5998cfa4-23d2-11e8-a6a3-ec086b02610b,33,Justin Brown,6f084ccc-5567-11e8-bc84-dca9047ef277,3,1024,747
  2011-07-12 13:11:16,599fbd89-23d2-11e8-a6a3-ec086b02610b.jpg,3,599fbd89-23d2-11e8-a6a3-ec086b02610b,46,Justin Brown,6f1728a1-5567-11e8-9be7-dca9047ef277,3,1024,747
  ```
- `train.csv` — 179423 rows; first lines:
  ```
  category_id,date_captured,file_name,frame_num,id,location,rights_holder,seq_id,seq_num_frames,width,height
  19,2012-03-17 03:48:44,588a679f-23d2-11e8-a6a3-ec086b02610b.jpg,2,588a679f-23d2-11e8-a6a3-ec086b02610b,115,Justin Brown,6f12067d-5567-11e8-b3c0-dca9047ef277,3,1024,747
  0,2014-05-11 11:56:46,59279ce3-23d2-11e8-a6a3-ec086b02610b.jpg,1,59279ce3-23d2-11e8-a6a3-ec086b02610b,96,Erin Boydston,6faa92d1-5567-11e8-b1ae-dca9047ef277,1,1024,747
  ```
Compressed artifacts:
- `test_images.zip` [compressed] (entries: 16862) — first entries: 5979bc71-23d2-11e8-a6a3-ec086b02610b.jpg, 59a49aaf-23d2-11e8-a6a3-ec086b02610b.jpg, 5a1640eb-23d2-11e8-a6a3-ec086b02610b.jpg, 5976a2fd-23d2-11e8-a6a3-ec086b02610b.jpg, 5a0e366f-23d2-11e8-a6a3-ec086b02610b.jpg
- `train_images.zip` [compressed] (entries: 179224) — first entries: 58cfcb4f-23d2-11e8-a6a3-ec086b02610b.jpg, 5965aaf2-23d2-11e8-a6a3-ec086b02610b.jpg, 5a0493b0-23d2-11e8-a6a3-ec086b02610b.jpg, 59da8a02-23d2-11e8-a6a3-ec086b02610b.jpg, 59ac6d3e-23d2-11e8-a6a3-ec086b02610b.jpg

## iwildcam-2020-fgvc7
Tables:
- `iwildcam2020_megadetector_results.json` — rows: n/a; first lines:
  ```
  ```
- `iwildcam2020_test_information.json` — rows: n/a; first lines:
  ```
  ```
- `iwildcam2020_train_annotations.json` — rows: n/a; first lines:
  ```
  ```
- `sample_submission.csv` — 60761 rows; first lines:
  ```
  Id,Category
  879d74d8-21bc-11ea-a13a-137349068a90,559
  90243894-21bc-11ea-a13a-137349068a90,629
  ```
Folders:
- `test/` — 60760 files, 0 subfolders; examples: 9472a2a0-21bc-11ea-a13a-137349068a90.jpg, 95b6d726-21bc-11ea-a13a-137349068a90.jpg, 9263b99a-21bc-11ea-a13a-137349068a90.jpg
- `train/` — 157199 files, 0 subfolders; examples: 87382b46-21bc-11ea-a13a-137349068a90.jpg, 96d7b936-21bc-11ea-a13a-137349068a90.jpg, 95dfbc72-21bc-11ea-a13a-137349068a90.jpg

## jigsaw-toxic-comment-classification-challenge
Tables:
- `sample_submission.csv` — 153165 rows; first lines:
  ```
  id,toxic,severe_toxic,obscene,threat,insult,identity_hate
  00001cee341fdb12,0.5,0.5,0.5,0.5,0.5,0.5
  0000247867823ef7,0.5,0.5,0.5,0.5,0.5,0.5
  ```
- `test.csv` — 552889 rows; first lines:
  ```
  id,comment_text
  00001cee341fdb12,Yo bitch Ja Rule is more succesful then you'll ever be whats up with you and hating you sad mofuckas...i should bitch slap ur pethedic white faces and get you to kiss my ass you guys …
  0000247867823ef7,== From RfC == 

 The title is fine as it is, IMO.
  ```
- `train.csv` — 561809 rows; first lines:
  ```
  id,comment_text,toxic,severe_toxic,obscene,threat,insult,identity_hate
  0000997932d777bf,Explanation
Why the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And pleas…
  000103f0d9cfb60f,D'aww! He matches this background colour I'm seemingly stuck with. Thanks.  (talk) 21:51, January 11, 2016 (UTC),0,0,0,0,0,0
  ```

## jigsaw-unintended-bias-in-toxicity-classification
Tables:
- `sample_submission.csv` — 97321 rows; first lines:
  ```
  id,prediction
  7097320,0.0
  7097321,0.0
  ```
- `test.csv` — 205781 rows; first lines:
  ```
  id,comment_text
  7097320,[ Integrity means that you pay your debts.]

Does this apply to President Trump too?
  7097321,This is malfeasance by the Administrator and the Board.  They are wasting our money!
  ```
- `train.csv` — 3820210 rows; first lines:
  ```
  id,target,comment_text,severe_toxicity,obscene,identity_attack,insult,threat,asian,atheist,bisexual,black,buddhist,christian,female,heterosexual,hindu,homosexual_gay_or_lesbian,intellectual_or_learnin…
  59848,0.0,This is so cool. It's like, 'would you want your mother to read this??' Really great idea, well done!,0.0,0.0,0.0,0.0,0.0,,,,,,,,,,,,,,,,,,,,,,,,,2015-09-29 10:50:41.987077+00,2,,2006,reject…
  59849,0.0,Thank you!! This would make my life a lot less anxiety-inducing. Keep it up, and don't let anyone get in your way!,0.0,0.0,0.0,0.0,0.0,,,,,,,,,,,,,,,,,,,,,,,,,2015-09-29 10:50:42.870083+00,2…
  ```

## kuzushiji-recognition
Tables:
- `sample_submission.csv` — 362 rows; first lines:
  ```
  image_id,labels
  umgy007-028,U+003F 1 1 U+FF2F 2 2
  hnsd004-026,U+003F 1 1 U+FF2F 2 2
  ```
- `train.csv` — 3245 rows; first lines:
  ```
  image_id,labels
  200004148_00015_1,U+306F 1187 361 47 27 U+306F 1487 2581 48 28 U+3070 1187 1063 74 30 U+3070 594 1154 93 31 U+306F 1192 1842 52 32 U+309D 755 2601 24 33 U+3070 1336 531 88 33 U+3044 1326 444 60 34 U+5…
  200021712-00008_2,U+4E00 1543 1987 58 11 U+4E00 1296 1068 91 11 U+4E00 1535 3266 67 14 U+4E00 531 1063 98 14 U+56DB 968 1982 77 32 U+4E8C 1343 1994 65 36 U+56DB 1165 3245 65 44 U+4E09 1337 3229 74 44 …
  ```
- `unicode_translation.csv` — 4782 rows; first lines:
  ```
  Unicode,char
  U+0031,1
  U+0032,2
  ```
Compressed artifacts:
- `test_images.zip` [compressed] (entries: 361) — first entries: 100249537_00079_1.jpg, 200014740-00086_1.jpg, umgy008-001.jpg, 200015779_00006_2.jpg, 200004148_00089_2.jpg
- `train_images.zip` [compressed] (entries: 3244) — first entries: 200014740-00044_2.jpg, 200021925-00011_2.jpg, hnsd010-014.jpg, umgy007-042.jpg, 100249537_00081_1.jpg

## leaf-classification
Tables:
- `sample_submission.csv` — 100 rows; first lines:
  ```
  id,Acer_Capillipes,Acer_Circinatum,Acer_Mono,Acer_Opalus,Acer_Palmatum,Acer_Pictum,Acer_Platanoids,Acer_Rubrum,Acer_Rufinerve,Acer_Saccharinum,Alnus_Cordata,Alnus_Maximowiczii,Alnus_Rubra,Alnus_Siebol…
  1202,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.0101…
  992,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.010101010101010102,0.01010…
  ```
- `test.csv` — 100 rows; first lines:
  ```
  id,margin1,margin2,margin3,margin4,margin5,margin6,margin7,margin8,margin9,margin10,margin11,margin12,margin13,margin14,margin15,margin16,margin17,margin18,margin19,margin20,margin21,margin22,margin23…
  1202,0.013672,0.03125,0.087891,0.013672,0.001953,0.021484,0.03125,0.001953,0.003906,0.035156,0.029297,0.007812,0.0625,0.0,0.019531,0.0,0.013672,0.021484,0.005859,0.011719,0.009766,0.001953,0.0,0.0,0.0…
  992,0.003906,0.007812,0.023438,0.066406,0.050781,0.029297,0.001953,0.003906,0.007812,0.005859,0.009766,0.0,0.037109,0.001953,0.007812,0.0,0.025391,0.019531,0.015625,0.007812,0.0,0.0,0.0,0.0,0.003906,0…
  ```
- `train.csv` — 892 rows; first lines:
  ```
  id,species,margin1,margin2,margin3,margin4,margin5,margin6,margin7,margin8,margin9,margin10,margin11,margin12,margin13,margin14,margin15,margin16,margin17,margin18,margin19,margin20,margin21,margin22,…
  186,Alnus_Cordata,0.001953,0.005859,0.039062,0.019531,0.025391,0.001953,0.058594,0.0,0.0,0.03125,0.015625,0.009766,0.013672,0.0,0.021484,0.0,0.023438,0.015625,0.003906,0.017578,0.003906,0.0,0.0,0.0039…
  1152,Tilia_Platyphyllos,0.001953,0.011719,0.023438,0.033203,0.056641,0.003906,0.03125,0.0,0.005859,0.035156,0.005859,0.017578,0.007812,0.001953,0.021484,0.0,0.013672,0.0,0.003906,0.007812,0.03125,0.0,…
  ```
Folders:
- `images/` — 990 files, 0 subfolders; examples: 357.jpg, 1062.jpg, 43.jpg

## learning-agency-lab-automated-essay-scoring-2
Tables:
- `sample_submission.csv` — 1732 rows; first lines:
  ```
  essay_id,score
  d550b2d,4
  0c10954,5
  ```
- `test.csv` — 15336 rows; first lines:
  ```
  essay_id,full_text
  d550b2d,The face was not created by aliens because there is still no proof that aliens or any living thing that lives on mars NASA are still looking for life on mars so how can the face be made by mar…
  0c10954,Hello my name is Luke Bomberger and I was seagoing cowboy after World War II. I helped transfer animals to Europe and Asia .It was after the war ,"and many countries were left in ruins".(parag…
  ```
- `train.csv` — 139231 rows; first lines:
  ```
  essay_id,full_text,score
  663d2cf,Dear State Senator,

I am arguing in favor of changing the electorol college to election by popular vote for the preesident of the united states. Over 60 percent of voters would prefer a direc…
  3a20bfb,In " The Challenge of Exploring Venus" The author suggests that studying Venus is a worthy pursuit despite the dangers that Venus represents.

In the text it gives multiple reasons that Venus …
  ```

## lmsys-chatbot-arena
Tables:
- `sample_submission.csv` — 5749 rows; first lines:
  ```
  id,winner_model_a,winner_model_b,winner_tie
  3297560222,0.3333333333333333,0.3333333333333333,0.3333333333333333
  2556155375,0.3333333333333333,0.3333333333333333,0.3333333333333333
  ```
- `test.csv` — 5749 rows; first lines:
  ```
  id,prompt,response_a,response_b
  3297560222,["What can you tell me about Maarten van Vulpen?","What do you know about Fonto?"],["Maarten van Vulpen (also spelled Marten or Martin) was a Dutch Golden Age painter, mainly known for his …
  2556155375,["is cebu island a good place to travel to in late november\/early december?","when would be the best time to visit","how is nightlife there? and dating\/hook up culture?"],["Yes, Cebu Isla…
  ```
- `train.csv` — 51730 rows; first lines:
  ```
  id,model_a,model_b,prompt,response_a,response_b,winner_model_a,winner_model_b,winner_tie
  2444074745,zephyr-7b-beta,llama-2-7b-chat,["Can the Orca Cloud Security Platform detect and remediate permissive storage configurations such as: Storage accounts with public access?"],["Yes, the Orca …
  1805535695,gpt-3.5-turbo-0613,llama-2-13b-chat,["Write 3 sensational twists for a thriller ","Si je te dis \" Melbourne 1 ticket for all zones\", et que je te demande d'extraire en json la nature du t…
  ```

## ml2021spring-hw2
Tables:
- `sampleSubmission.csv` — 330292 rows; first lines:
  ```
  Id,ClassId
  0,0
  1,0
  ```
Folders:
- `timit_11/` — 0 files, 1 subfolders; examples: timit_11/test_11.npy

## mlsp-2013-birds
Tables:
- `sample_submission.csv` — 1217 rows; first lines:
  ```
  Id,Probability
  100,0
  101,0
  ```
Folders:
- `essential_data/` — 4 files, 1 subfolders; examples: rec_labels_test_hidden.txt, CVfolds_2.txt, species_list.txt
- `supplemental_data/` — 5 files, 4 subfolders; examples: segment_mosaic.bmp, segment_features.txt, segment_clusters.bmp

## movie-review-sentiment-analysis-kernels-only
Tables:
- `sampleSubmission.csv` — 46819 rows; first lines:
  ```
  PhraseId,Sentiment
  21924,2
  18207,2
  ```
- `test.tsv (inside test.tsv.zip)` — 46819 rows; first lines:
  ```
  PhraseId SentenceId Phrase
  21924 980 escape movie
  18207 795 well-executed
  ```
- `train.tsv (inside train.tsv.zip)` — 109243 rows; first lines:
  ```
  PhraseId SentenceId Phrase Sentiment
  24144 1097 through every frame 2
  85111 4402 onscreen presence 2
  ```
Compressed artifacts:
- `test.tsv.zip` [compressed] (entries: 1) — first entries: test.tsv
- `train.tsv.zip` [compressed] (entries: 1) — first entries: train.tsv

## multi-modal-gesture-recognition
Tables:
- `randomPredictions.csv` — 96 rows; first lines:
  ```
  Id,Sequence
  0300,13 14 2 9 16 7 20 5 8 6 10 4 3 12 18 1 15 17 19 11
  0301,4 3 11 16 20 6 7 15 10 18 17 9 8 12 5 19 1 13 14 2
  ```
- `test.csv` — 96 rows; first lines:
  ```
  Id
  0300
  0301
  ```
- `training.csv` — 298 rows; first lines:
  ```
  Id,Sequence
  0001,2 14 20 6 7 3 1 13 18 5 12 16 15 4 9 10 8 17 19 11
  0003,12 3 18 14 16 20 5 2 4 1 10 6 9 19 15 17 11 13 8 7
  ```
Compressed artifacts:
- `sample_code_mmrgc.zip` [compressed] (entries: 9) — first entries: sample_code_mmrgc_working/, sample_code_mmrgc_working/dtw.m, sample_code_mmrgc_working/extract_zip_files.m, sample_code_mmrgc_working/getGestureID.m, sample_code_mmrgc_working/load_challenge_data.m
- `test.tar.gz` [compressed] (entries: 95) — first entries: ./Sample00300.zip, ./Sample00301.zip, ./Sample00302.zip, ./Sample00303.zip, ./Sample00304.zip
- `training1.tar.gz` [compressed] (entries: 99) — first entries: ./Sample00001.zip, ./Sample00003.zip, ./Sample00004.zip, ./Sample00005.zip, ./Sample00006.zip
- `training2.tar.gz` [compressed] (entries: 99) — first entries: ./Sample00101.zip, ./Sample00102.zip, ./Sample00103.zip, ./Sample00104.zip, ./Sample00105.zip
- `training3.tar.gz` [compressed] (entries: 100) — first entries: ./Sample00200.zip, ./Sample00201.zip, ./Sample00202.zip, ./Sample00203.zip, ./Sample00204.zip
- `validation1.tar.gz` [compressed] (entries: 99) — first entries: Sample00410.zip, Sample00411.zip, Sample00412.zip, Sample00413.zip, Sample00414.zip
- `validation2.tar.gz` [compressed] (entries: 104) — first entries: Sample00510.zip, Sample00516.zip, Sample00517.zip, Sample00518.zip, Sample00519.zip
- `validation3.tar.gz` [compressed] (entries: 84) — first entries: Sample00621.zip, Sample00622.zip, Sample00623.zip, Sample00624.zip, Sample00625.zip

## new-york-city-taxi-fare-prediction
Tables:
- `labels.csv` — 55413943 rows; first lines:
  ```
  key,fare_amount,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
  2014-03-30 12:14:00.000000128,4.5,2014-03-30 12:14:00 UTC,-73.988372,40.77446,-73.983295,40.76763,6
  2009-09-25 22:18:00.0000008,4.5,2009-09-25 22:18:00 UTC,-73.971122,40.675378,-73.978622,40.663852,5
  ```
- `sample_submission.csv` — 9915 rows; first lines:
  ```
  key,fare_amount
  2010-10-01 21:26:11.0000001,11.35
  2013-10-06 01:38:00.00000083,11.35
  ```
- `test.csv` — 9915 rows; first lines:
  ```
  key,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count
  2010-10-01 21:26:11.0000001,2010-10-01 21:26:11 UTC,-73.98313,40.76197,-73.994386,40.749236,1
  2013-10-06 01:38:00.00000083,2013-10-06 01:38:00 UTC,-73.948505,40.753977,-73.808195,40.731952,2
  ```

## nfl-player-contact-detection
Tables:
- `sample_submission.csv` — 463244 rows; first lines:
  ```
  contact_id,contact
  58187_001341_0_47795_52650,0
  58187_001341_0_47795_47804,0
  ```
- `test_baseline_helmets.csv` — 371409 rows; first lines:
  ```
  game_play,game_key,play_id,view,video,frame,nfl_player_id,player_label,left,width,top,height
  58187_001341,58187,1341,Endzone,58187_001341_Endzone.mp4,290,43426,H94,433,26,350,19
  58187_001341,58187,1341,Endzone,58187_001341_Endzone.mp4,290,52650,H53,132,26,324,23
  ```
- `test_player_tracking.csv` — 127755 rows; first lines:
  ```
  game_play,game_key,play_id,nfl_player_id,datetime,step,team,position,jersey_number,x_position,y_position,speed,distance,direction,orientation,acceleration,sa
  58266_000095,58266,95,42390,2020-11-15T21:07:04.200Z,-170,home,SS,21,31.43,25.96,0.2,0.02,136.56,194.84,0.16,-0.16
  58266_000095,58266,95,43308,2020-11-15T21:07:04.200Z,-170,home,OLB,90,26.99,25.07,0.41,0.04,224.19,188.0,0.26,0.26
  ```
- `test_video_metadata.csv` — 49 rows; first lines:
  ```
  game_play,game_key,play_id,view,start_time,end_time,snap_time
  58187_001341,58187,1341,Endzone,2020-09-20T17:54:57.267Z,2020-09-20T17:55:09.449Z,2020-09-20T17:55:02.267Z
  58187_001341,58187,1341,Sideline,2020-09-20T17:54:57.267Z,2020-09-20T17:55:09.449Z,2020-09-20T17:55:02.267Z
  ```
- `train_baseline_helmets.csv` — 3412209 rows; first lines:
  ```
  game_play,game_key,play_id,view,video,frame,nfl_player_id,player_label,left,width,top,height
  58168_003392,58168,3392,Endzone,58168_003392_Endzone.mp4,290,39947,H72,946,25,293,34
  58168_003392,58168,3392,Endzone,58168_003392_Endzone.mp4,290,37211,H42,151,25,267,33
  ```
- `train_labels.csv` — 4258376 rows; first lines:
  ```
  contact_id,game_play,datetime,step,nfl_player_id_1,nfl_player_id_2,contact
  58168_003392_0_38590_43854,58168_003392,2020-09-11T03:01:48.100Z,0,38590,43854,0
  58168_003392_0_38590_41257,58168_003392,2020-09-11T03:01:48.100Z,0,38590,41257,0
  ```
- `train_player_tracking.csv` — 1225300 rows; first lines:
  ```
  game_play,game_key,play_id,nfl_player_id,datetime,step,team,position,jersey_number,x_position,y_position,speed,distance,direction,orientation,acceleration,sa
  58580_001136,58580,1136,44830,2021-10-10T21:08:20.900Z,-108,away,CB,22,61.59,42.6,1.11,0.11,320.33,263.93,0.71,-0.64
  58580_001136,58580,1136,47800,2021-10-10T21:08:20.900Z,-108,away,DE,97,59.48,26.81,0.23,0.01,346.84,247.16,1.29,0.9
  ```
- `train_video_metadata.csv` — 433 rows; first lines:
  ```
  game_play,game_key,play_id,view,start_time,end_time,snap_time
  58168_003392,58168,3392,Endzone,2020-09-11T03:01:43.134Z,2020-09-11T03:01:54.971Z,2020-09-11T03:01:48.134Z
  58168_003392,58168,3392,Sideline,2020-09-11T03:01:43.134Z,2020-09-11T03:01:54.971Z,2020-09-11T03:01:48.134Z
  ```
Folders:
- `test/` — 72 files, 0 subfolders; examples: 58187_001341_Endzone.mp4, 58544_002496_Sideline.mp4, 58187_001341_Sideline.mp4
- `train/` — 648 files, 0 subfolders; examples: 58218_003210_Sideline.mp4, 58285_004176_Sideline.mp4, 58553_001995_Endzone.mp4

## nomad2018-predict-transparent-conductors
Tables:
- `sample_submission.csv` — 241 rows; first lines:
  ```
  id,formation_energy_ev_natom,bandgap_energy_ev
  1,0.1779,1.8892
  2,0.1779,1.8892
  ```
- `test.csv` — 241 rows; first lines:
  ```
  id,spacegroup,number_of_total_atoms,percent_atom_al,percent_atom_ga,percent_atom_in,lattice_vector_1_ang,lattice_vector_2_ang,lattice_vector_3_ang,lattice_angle_alpha_degree,lattice_angle_beta_degree,…
  1,33,40.0,0.5,0.0625,0.4375,5.248,8.9682,9.5964,90.0031,90.0004,90.0006
  2,33,80.0,0.4062,0.1562,0.4375,10.5398,9.0056,9.6321,90.0022,90.0002,90.0005
  ```
- `train.csv` — 2161 rows; first lines:
  ```
  id,spacegroup,number_of_total_atoms,percent_atom_al,percent_atom_ga,percent_atom_in,lattice_vector_1_ang,lattice_vector_2_ang,lattice_vector_3_ang,lattice_angle_alpha_degree,lattice_angle_beta_degree,…
  1,206,80.0,0.3125,0.625,0.0625,9.3282,9.3279,9.3277,90.0047,90.0045,89.995,0.1337,2.6562
  2,206,80.0,1.0,0.0,0.0,8.9847,8.9839,8.9843,90.0024,90.0036,89.9994,0.0738,5.2114
  ```
Folders:
- `test/` — 0 files, 240 subfolders; examples: 8/geometry.xyz, 49/geometry.xyz, 199/geometry.xyz
- `train/` — 0 files, 2160 subfolders; examples: 2035/geometry.xyz, 1025/geometry.xyz, 1910/geometry.xyz

## osic-pulmonary-fibrosis-progression
Tables:
- `sample_submission.csv` — 1909 rows; first lines:
  ```
  Patient_Week,FVC,Confidence
  ID00126637202218610655908_-3,2000,100
  ID00126637202218610655908_-2,2000,100
  ```
- `test.csv` — 19 rows; first lines:
  ```
  Patient,Weeks,FVC,Percent,Age,Sex,SmokingStatus
  ID00014637202177757139317,0,3807,90.076660988075,56,Male,Ex-smoker
  ID00019637202178323708467,13,2100,92.8587220871103,83,Female,Ex-smoker
  ```
- `train.csv` — 1395 rows; first lines:
  ```
  Patient,Weeks,FVC,Percent,Age,Sex,SmokingStatus
  ID00133637202223847701934,-2,3195,92.8563124854685,83,Male,Never smoked
  ID00133637202223847701934,2,3203,93.0888165542897,83,Male,Never smoked
  ```
Folders:
- `test/` — 0 files, 18 subfolders; examples: ID00127637202219096738943/26.dcm, ID00126637202218610655908/14.dcm, ID00364637202296074419422/26.dcm
- `train/` — 0 files, 158 subfolders; examples: ID00343637202287577133798/26.dcm, ID00340637202287399835821/26.dcm, ID00368637202296470751086/238.dcm

## paddy-disease-classification
Tables:
- `sample_submission.csv` — 2603 rows; first lines:
  ```
  image_id,label
  101853.jpg,
  105016.jpg,
  ```
- `train.csv` — 7806 rows; first lines:
  ```
  image_id,label,variety,age
  110054.jpg,blast,Ponni,47
  100093.jpg,brown_spot,ADT45,68
  ```
Folders:
- `test_images/` — 2602 files, 0 subfolders; examples: 105221.jpg, 109825.jpg, 106668.jpg
- `train_images/` — 0 files, 10 subfolders; examples: bacterial_leaf_streak/110210.jpg, dead_heart/102406.jpg, bacterial_panicle_blight/110121.jpg

## petfinder-pawpularity-score
Tables:
- `sample_submission.csv` — 993 rows; first lines:
  ```
  Id,Pawpularity
  ee51b99832f1ba868f646df93d2b6b81,64.06
  caddfb3f8bff9c4b95dbe022018eea21,27.71
  ```
- `test.csv` — 993 rows; first lines:
  ```
  Id,Subject Focus,Eyes,Face,Near,Action,Accessory,Group,Collage,Human,Occlusion,Info,Blur
  ee51b99832f1ba868f646df93d2b6b81,0,1,1,1,0,0,0,0,0,0,0,0
  caddfb3f8bff9c4b95dbe022018eea21,0,0,1,1,0,1,1,0,0,0,0,0
  ```
- `train.csv` — 8921 rows; first lines:
  ```
  Id,Subject Focus,Eyes,Face,Near,Action,Accessory,Group,Collage,Human,Occlusion,Info,Blur,Pawpularity
  1a8795e64a294ed0c95132e18ee198e1,0,1,1,1,0,0,0,0,0,0,0,0,55
  08ce774252e822838bf598aa10518a11,0,1,1,1,0,0,0,0,0,0,0,0,100
  ```
Folders:
- `test/` — 992 files, 0 subfolders; examples: 46a5740a0334444ab0a79a314aad37c1.jpg, 39a6cac5a4f1191973fc62bc9bcf41ca.jpg, d8ef319a79cfee7d568270cd94452c3a.jpg
- `train/` — 8920 files, 0 subfolders; examples: ed22784634beaf4d0ef356257b16c32f.jpg, dd8d14e3e310dfa7526f838a68003f22.jpg, 950ac5df0ec4f96dfecc428a34deb22b.jpg

## plant-pathology-2020-fgvc7
Tables:
- `sample_submission.csv` — 184 rows; first lines:
  ```
  image_id,healthy,multiple_diseases,rust,scab
  Test_0,0.25,0.25,0.25,0.25
  Test_1,0.25,0.25,0.25,0.25
  ```
- `test.csv` — 184 rows; first lines:
  ```
  image_id
  Test_0
  Test_1
  ```
- `train.csv` — 1639 rows; first lines:
  ```
  image_id,healthy,multiple_diseases,rust,scab
  Train_0,0,0,1,0
  Train_1,1,0,0,0
  ```
Folders:
- `images/` — 1821 files, 0 subfolders; examples: Train_651.jpg, Train_218.jpg, Train_1113.jpg

## plant-pathology-2021-fgvc8
Tables:
- `sample_submission.csv` — 3728 rows; first lines:
  ```
  image,labels
  ca6a50c5d2adb8ae.jpg,healthy
  b686d217a1e2e3a5.jpg,healthy
  ```
- `train.csv` — 14906 rows; first lines:
  ```
  image,labels
  95cb4b75ad1d842a.jpg,complex
  be80d450dac87d7c.jpg,frog_eye_leaf_spot complex
  ```
Folders:
- `test_images/` — 3727 files, 0 subfolders; examples: e8bd8ac4d982dd83.jpg, 8ed644869ee5d14b.jpg, b4a1e947ce2d1e54.jpg
- `train_images/` — 14905 files, 0 subfolders; examples: acf29ac1c9ce2792.jpg, a26bd8e27025b3bc.jpg, ccdc9e82c2757562.jpg

## plant-seedlings-classification
Tables:
- `sample_submission.csv` — 667 rows; first lines:
  ```
  file,species
  f900b7684.png,Sugar beet
  9a8531ba0.png,Sugar beet
  ```
Folders:
- `test/` — 666 files, 0 subfolders; examples: fe2ad3d8c.png, c7344c2e3.png, 911a91de2.png
- `train/` — 0 files, 12 subfolders; examples: Common Chickweed/f3e74582f.png, Maize/3cf92e356.png, Scentless Mayweed/2a5938731.png

## playground-series-s3e18
Tables:
- `sample_submission.csv` — 1485 rows; first lines:
  ```
  id,EC1,EC2
  1377,0.5,0.5
  5485,0.5,0.5
  ```
- `test.csv` — 1485 rows; first lines:
  ```
  id,BertzCT,Chi1,Chi1n,Chi1v,Chi2n,Chi2v,Chi3v,Chi4n,EState_VSA1,EState_VSA2,ExactMolWt,FpDensityMorgan1,FpDensityMorgan2,FpDensityMorgan3,HallKierAlpha,HeavyAtomMolWt,Kappa3,MaxAbsEStateIndex,MinEStat…
  1377,221.2638658,7.413591358,5.874958511,5.874958511,2.861665709,2.861665709,1.786049894,1.058931007,5.969305288,17.91984529,222.0680796,1.555555556,2.222222222,2.666666667,-1.1,212.116,1.83950433,10.…
  5485,124.9343323,6.270856948,3.633935872,3.633935872,2.571552775,2.571552775,1.53955752,0.835261196,6.103966388,11.21924332,179.0793725,1.0,1.785714286,1.857142857,-0.02,166.068,8.615110047,10.7240192…
  ```
- `train.csv` — 13355 rows; first lines:
  ```
  id,BertzCT,Chi1,Chi1n,Chi1v,Chi2n,Chi2v,Chi3v,Chi4n,EState_VSA1,EState_VSA2,ExactMolWt,FpDensityMorgan1,FpDensityMorgan2,FpDensityMorgan3,HallKierAlpha,HeavyAtomMolWt,Kappa3,MaxAbsEStateIndex,MinEStat…
  3305,212.9284414,6.270856948,3.431698411,4.045502408,1.811731173,2.272429169,1.619489217,0.828834676,7.822697123,6.420821623,209.1164267,1.545454546,2.272727273,2.818181818,-0.01,194.125,5.58,10.89397…
  8217,221.6943549,4.060660172,3.548618073,3.548618073,2.499651759,2.499651759,1.607504151,0.883813474,17.98045141,0.0,171.0531578,1.25,1.916666667,2.416666667,-1.59,162.08,1.663742547,9.226851852,-1.16…
  ```

## predict-volcanic-eruptions-ingv-oe
Tables:
- `sample_submission.csv` — 445 rows; first lines:
  ```
  segment_id,time_to_eruption
  951290289,0
  508758258,0
  ```
- `train.csv` — 3988 rows; first lines:
  ```
  segment_id,time_to_eruption
  1410693848,20109998
  987159268,7202883
  ```
Folders:
- `test/` — 444 files, 0 subfolders; examples: 1963562520.csv, 922017943.csv, 1188262821.csv
- `train/` — 3987 files, 0 subfolders; examples: 1255705928.csv, 1098612833.csv, 198883212.csv

## random-acts-of-pizza
Tables:
- `sampleSubmission.csv` — 1163 rows; first lines:
  ```
  request_id,requester_received_pizza
  t3_1aw5zf,0
  t3_roiuw,0
  ```
- `test.json` — rows: n/a; first lines:
  ```
  [
      {
          "giver_username_if_known": "N/A",
  ```
- `test.json (inside test.zip)` — 44674 rows; first lines:
  ```
  [
      {
          "giver_username_if_known": "N/A",
  ```
- `train.json` — rows: n/a; first lines:
  ```
  [
      {
          "giver_username_if_known": "N/A",
  ```
- `train.json (inside train.zip)` — 151601 rows; first lines:
  ```
  [
      {
          "giver_username_if_known": "N/A",
  ```
Compressed artifacts:
- `test.zip` [compressed] (entries: 1) — first entries: test.json
- `train.zip` [compressed] (entries: 1) — first entries: train.json

## ranzcr-clip-catheter-line-classification
Tables:
- `sample_submission.csv` — 3010 rows; first lines:
  ```
  StudyInstanceUID,ETT - Abnormal,ETT - Borderline,ETT - Normal,NGT - Abnormal,NGT - Borderline,NGT - Incompletely Imaged,NGT - Normal,CVC - Abnormal,CVC - Borderline
  1.2.826.0.1.3680043.8.498.25512976433640891933030328516792246363,0,0,0,0,0,0,0,0,0
  1.2.826.0.1.3680043.8.498.24449897997512078380656427106792860945,0,0,0,0,0,0,0,0,0
  ```
- `train.csv` — 27075 rows; first lines:
  ```
  StudyInstanceUID,ETT - Abnormal,ETT - Borderline,ETT - Normal,NGT - Abnormal,NGT - Borderline,NGT - Incompletely Imaged,NGT - Normal,CVC - Abnormal,CVC - Borderline,CVC - Normal,Swan Ganz Catheter Pre…
  1.2.826.0.1.3680043.8.498.93452244702936724316366868659274348219,0,0,0,0,0,0,0,1,0,0,0,258689f05
  1.2.826.0.1.3680043.8.498.93702111677661381919780459258465903595,0,0,0,0,0,0,0,0,1,0,0,6df02c500
  ```
- `train_annotations.csv` — 16262 rows; first lines:
  ```
  StudyInstanceUID,label,data
  1.2.826.0.1.3680043.8.498.12616281126973421762775197134528405307,CVC - Normal,[[1487, 1279], [1477, 1168], [1472, 1052], [1464, 924], [1453, 827], [1443, 755], [1434, 640], [1404, 514], [1387, 497], […
  1.2.826.0.1.3680043.8.498.12616281126973421762775197134528405307,CVC - Normal,[[1328, 7], [1347, 101], [1383, 193], [1400, 267], [1411, 366], [1400, 428], [1387, 545], [1394, 640], [1400, 707], [1417,…
  ```
Folders:
- `test/` — 3009 files, 0 subfolders; examples: 1.2.826.0.1.3680043.8.498.56835462899690749163459354373299557611.jpg, 1.2.826.0.1.3680043.8.498.96706195987855079925749546279373631561.jpg, 1.2.826.0.1.3680043.8.498.60060685570122927098628701306261231082.jpg
- `train/` — 27074 files, 0 subfolders; examples: 1.2.826.0.1.3680043.8.498.85828226541800789119342654641033381493.jpg, 1.2.826.0.1.3680043.8.498.11622564736419184787101018148754924205.jpg, 1.2.826.0.1.3680043.8.498.97278161428071164646024646659788885575.jpg

## rsna-2022-cervical-spine-fracture-detection
Tables:
- `sample_submission.csv` — 14537 rows; first lines:
  ```
  row_id,fractured
  1.2.826.0.1.3680043.6200_patient_overall,0.5
  1.2.826.0.1.3680043.27262_patient_overall,0.5
  ```
- `test.csv` — 14537 rows; first lines:
  ```
  StudyInstanceUID,prediction_type,row_id
  1.2.826.0.1.3680043.6200,patient_overall,1.2.826.0.1.3680043.6200_patient_overall
  1.2.826.0.1.3680043.27262,patient_overall,1.2.826.0.1.3680043.27262_patient_overall
  ```
- `train.csv` — 203 rows; first lines:
  ```
  StudyInstanceUID,patient_overall,C1,C2,C3,C4,C5,C6,C7
  1.2.826.0.1.3680043.21561,1,0,1,0,0,0,0,0
  1.2.826.0.1.3680043.9447,1,0,1,0,0,0,0,0
  ```
- `train_bounding_boxes.csv` — 691 rows; first lines:
  ```
  StudyInstanceUID,x,y,width,height,slice_number
  1.2.826.0.1.3680043.12152,177.0,242.0,107.0,96.0,330
  1.2.826.0.1.3680043.12152,178.0,243.0,106.0,94.0,331
  ```
Folders:
- `segmentations/` — 9 files, 0 subfolders; examples: 1.2.826.0.1.3680043.24617.nii, 1.2.826.0.1.3680043.26110.nii, 1.2.826.0.1.3680043.30487.nii
- `test_images/` — 0 files, 1817 subfolders; examples: 1.2.826.0.1.3680043.5647/347.dcm, 1.2.826.0.1.3680043.13447/238.dcm, 1.2.826.0.1.3680043.17127/238.dcm
- `train_images/` — 0 files, 202 subfolders; examples: 1.2.826.0.1.3680043.7343/56.dcm, 1.2.826.0.1.3680043.19596/347.dcm, 1.2.826.0.1.3680043.19705/238.dcm

## rsna-breast-cancer-detection
Tables:
- `sample_submission.csv` — 2385 rows; first lines:
  ```
  prediction_id,cancer
  10116_L,0.02057604809879753
  10116_R,0.02057604809879753
  ```
- `test.csv` — 5475 rows; first lines:
  ```
  site_id,patient_id,image_id,laterality,view,age,implant,machine_id,prediction_id
  2,10116,472095321,L,CC,67.0,0,29,10116_L
  2,10116,539757861,L,MLO,67.0,0,29,10116_L
  ```
- `train.csv` — 49233 rows; first lines:
  ```
  site_id,patient_id,image_id,laterality,view,age,cancer,biopsy,invasive,BIRADS,implant,density,machine_id,difficult_negative_case
  2,10006,462822612,L,CC,61.0,0,0,0,,0,,29,False
  2,10006,1459541791,L,MLO,61.0,0,0,0,,0,,29,False
  ```
Folders:
- `test_images/` — 0 files, 1192 subfolders; examples: 2035/1771983968.dcm, 1025/1122776493.dcm, 31944/917770332.dcm
- `train_images/` — 0 files, 10721 subfolders; examples: 25238/1167696805.dcm, 33266/524725288.dcm, 42723/1472342200.dcm

## rsna-miccai-brain-tumor-radiogenomic-classification
Tables:
- `sample_submission.csv` — 60 rows; first lines:
  ```
  BraTS21ID,MGMT_value
  00356,0.5
  00140,0.5
  ```
- `train_labels.csv` — 527 rows; first lines:
  ```
  BraTS21ID,MGMT_value
  00642,0
  00100,1
  ```
Folders:
- `test/` — 0 files, 59 subfolders; examples: 00177/T2w, 00263/T2w, 00185/T2w
- `train/` — 0 files, 526 subfolders; examples: 00380/T2w, 00577/T2w, 00652/T2w

## seti-breakthrough-listen
Tables:
- `sample_submission.csv` — 6001 rows; first lines:
  ```
  id,target
  0cee567456cd304,0.5
  5451b45281c65a7,0.5
  ```
- `train_labels.csv` — 54001 rows; first lines:
  ```
  id,target
  d5d85dafc41d5b3,0
  6170c3d29bd5874,0
  ```
Folders:
- `old_leaky_data/` — 2 files, 2 subfolders; examples: train_labels_old.csv, test_labels_old.csv, test_old/8
- `test/` — 0 files, 16 subfolders; examples: 8/8ca007b834cafff.npy, 5/5dca3c2fd520fe1.npy, e/e2f8f5d4f7910cc.npy
- `train/` — 0 files, 16 subfolders; examples: 8/8037e6388974c33.npy, 5/578422367ec6290.npy, e/eca36d4df2ca24d.npy

## siim-covid19-detection
Tables:
- `sample_submission.csv` — 1245 rows; first lines:
  ```
  id,PredictionString
  000c9c05fd14_study,negative 1 0 0 1 1
  00c74279c5b7_study,negative 1 0 0 1 1
  ```
- `train_image_level.csv` — 5697 rows; first lines:
  ```
  id,boxes,label,StudyInstanceUID
  000a312787f2_image,[{'x': 789.28836, 'y': 582.43035, 'width': 1026.65662, 'height': 1917.30292}, {'x': 2245.91208, 'y': 591.20528, 'width': 1094.66162, 'height': 1761.54944}],opacity 1 789.28836 582.4…
  000c3a3f293f_image,,none 1 0 0 1 1,ff0879eb20ed
  ```
- `train_study_level.csv` — 5449 rows; first lines:
  ```
  id,Negative for Pneumonia,Typical Appearance,Indeterminate Appearance,Atypical Appearance
  00086460a852_study,0,1,0,0
  00292f8c37bd_study,1,0,0,0
  ```
Folders:
- `test/` — 0 files, 606 subfolders; examples: d2cf237688a4/3fde77b139aa, 19c6a6e0cb1c/19a0d3f15181, 542d1e88c511/da9629dfec8e
- `train/` — 0 files, 5448 subfolders; examples: c39d68397d84/f53ede954f64, dc2b14b11aaf/d5632d22c238, 980351f05de0/836bbf127ab8

## siim-isic-melanoma-classification
Tables:
- `sample_submission.csv` — 4143 rows; first lines:
  ```
  image_name,target
  ISIC_0052212,0
  ISIC_0076545,0
  ```
- `test.csv` — 4143 rows; first lines:
  ```
  image_name,patient_id,sex,age_approx,anatom_site_general_challenge
  ISIC_0052212,IP_2842074,female,50.0,lower extremity
  ISIC_0076545,IP_9802602,male,55.0,upper extremity
  ```
- `train.csv` — 28985 rows; first lines:
  ```
  image_name,patient_id,sex,age_approx,anatom_site_general_challenge,diagnosis,benign_malignant,target
  ISIC_2637011,IP_7279968,male,45.0,head/neck,unknown,benign,0
  ISIC_0015719,IP_3075186,female,45.0,upper extremity,unknown,benign,0
  ```
Folders:
- `jpeg/` — 0 files, 2 subfolders; examples: train/ISIC_8904326.jpg, test/ISIC_5107655.jpg
- `test/` — 4142 files, 0 subfolders; examples: ISIC_3171941.dcm, ISIC_2998670.dcm, ISIC_1535599.dcm
- `tfrecords/` — 16 files, 0 subfolders; examples: train09-2071.tfrec, train02-2071.tfrec, train12-2071.tfrec
- `train/` — 28984 files, 0 subfolders; examples: ISIC_7830756.dcm, ISIC_1070864.dcm, ISIC_4330291.dcm

## smartphone-decimeter-2022
Tables:
- `sample_submission.csv` — 37088 rows; first lines:
  ```
  tripId,UnixTimeMillis,LatitudeDegrees,LongitudeDegrees
  2020-06-04-US-MTV-1-GooglePixel4,1591304310441,37.904611315634504,-86.48107806249548
  2020-06-04-US-MTV-1-GooglePixel4,1591304311441,37.904611315634504,-86.48107806249548
  ```
Folders:
- `metadata/` — 3 files, 0 subfolders; examples: raw_state_bit_map.json, constellation_type_mapping.csv, accumulated_delta_range_state_bit_map.json
- `test/` — 0 files, 8 subfolders; examples: 2020-07-08-US-MTV-1/GooglePixel4, 2020-06-04-US-MTV-1/GooglePixel4, 2021-04-29-US-MTV-1/XiaomiMi8
- `train/` — 0 files, 54 subfolders; examples: 2021-07-19-US-MTV-1/XiaomiMi8, 2021-03-16-US-MTV-1/XiaomiMi8, 2021-07-14-US-MTV-1/XiaomiMi8

## spaceship-titanic
Tables:
- `sample_submission.csv` — 871 rows; first lines:
  ```
  PassengerId,Transported
  3868_05,False
  6405_02,False
  ```
- `test.csv` — 871 rows; first lines:
  ```
  PassengerId,HomePlanet,CryoSleep,Cabin,Destination,Age,VIP,RoomService,FoodCourt,ShoppingMall,Spa,VRDeck,Name
  3868_05,Earth,False,F/731/S,55 Cancri e,16.0,False,0.0,0.0,623.0,40.0,209.0,Darry Braymon
  6405_02,Earth,,,,2.0,False,0.0,0.0,0.0,0.0,0.0,Feline Toddleton
  ```
- `train.csv` — 7824 rows; first lines:
  ```
  PassengerId,HomePlanet,CryoSleep,Cabin,Destination,Age,VIP,RoomService,FoodCourt,ShoppingMall,Spa,VRDeck,Name,Transported
  4408_01,Mars,True,F/906/P,TRAPPIST-1e,75.0,False,0.0,0.0,0.0,0.0,0.0,Pich Knike,True
  7710_01,Europa,False,B/253/P,TRAPPIST-1e,27.0,False,118.0,1769.0,4127.0,118.0,619.0,Chabih Eguing,True
  ```

## spooky-author-identification
Tables:
- `sample_submission.csv` — 1959 rows; first lines:
  ```
  id,EAP,HPL,MWS
  id27251,0.403493538995863,0.287808366106543,0.308698094897594
  id09612,0.403493538995863,0.287808366106543,0.308698094897594
  ```
- `test.csv` — 1959 rows; first lines:
  ```
  id,text
  id27251,There seemed to be a void, and nothing more, and I felt a childish fear which prompted me to draw from my hip pocket the revolver I always carried after dark since the night I was held up in E…
  id09612,This event caused many of those who were about to sail, to put foot again on firm land, ready to encounter any evil rather than to rush into the yawning jaws of the pitiless ocean.
  ```
- `train.csv` — 17622 rows; first lines:
  ```
  id,text,author
  id06121,So I did not abandon the search until I had become fully satisfied that the thief is a more astute man than myself.,EAP
  id01074,He had promised to spend some hours with me one afternoon but a violent and continual rain prevented him.,MWS
  ```

## stanford-covid-vaccine
Tables:
- `sample_submission.csv` — 25681 rows; first lines:
  ```
  id_seqpos,reactivity,deg_Mg_pH10,deg_pH10,deg_Mg_50C,deg_50C
  id_00b436dec_0,0.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000
  id_00b436dec_1,0.0000000000,0.0000000000,0.0000000000,0.0000000000,0.0000000000
  ```
- `test.json` — rows: n/a; first lines:
  ```
  {"index":0,"id":"id_00b436dec","sequence":"GGAAAUCAUCGAGGACGGGUCCGUUCAGCACGCGAAAGCGUCGUGAACGGACACAAGUCCUCGAUGAACGAAUGCUUCGGCGUUCGAAAAGAAACAACAACAACAAC","structure":".....(((((((((((..(((((((((..((((..…
  {"index":1,"id":"id_010ab0472","sequence":"GGAAAGCAUGGGACCACGAUUCACAUCGGUCUGCACGUAGGACAUUCUUGUAGUUAGGUUCUACGUCAAUGGGAGUUCGCUUCUAUAAAAGAAACAACAACAACAAC","structure":".....(((...((((..(((....))))))))))(…
  {"index":2,"id":"id_01ccf95c0","sequence":"GGAAAAGCGAACGACGAAACGCGGGCGCGAUGGACAGGAGGCUGACACCCAGCGGACUGGACGUCAAAGGCCGGCUUCGGCUGGCCAAAAGAAACAACAACAACAAC","structure":"......(((..((.((...))))..)))((((..(…
  ```
- `train.json` — rows: n/a; first lines:
  ```
  {"index":0,"id":"id_001f94081","sequence":"GGAAAAGCUCUAAUAACAGGAGACUAGGACUACGUAUUUCUAGGUAACUGGAAUAACCCAUACCAGCAGUUAGAGUUCGCUCUAACAAAAGAAACAACAACAACAAC","structure":".....((((((.......)))).)).((.....((…
  {"index":1,"id":"id_0049f53ba","sequence":"GGAAAAAGCGCGCGCGGUUAGCGCGCGCUUUUGCGCGCGCUGUACCGCGCGCGCUUAUGCAAGUUGCCCGCGGCGUUCGCGCUGUGAAAAGAAACAACAACAACAAC","structure":".....(((((((((((((((((((((((....)))…
  {"index":2,"id":"id_006f36f57","sequence":"GGAAAGUGCUCAGAUAAGCUAAGCUCGAAUAGCAAUCGAAUAGAAUCGAAAUAGCAUCGAUGUGUAUAUGGGUGGUUCGCCGCUCAAAAAGAAACAACAACAACAAC","structure":".....((((.((.....((((.(((.....)))..…
  ```

## statoil-iceberg-classifier-challenge

## tabular-playground-series-dec-2021
Tables:
- `sample_submission.csv` — 400001 rows; first lines:
  ```
  Id,Cover_Type
  814683,2
  1357371,2
  ```
- `test.csv` — 400001 rows; first lines:
  ```
  Id,Elevation,Aspect,Slope,Horizontal_Distance_To_Hydrology,Vertical_Distance_To_Hydrology,Horizontal_Distance_To_Roadways,Hillshade_9am,Hillshade_Noon,Hillshade_3pm,Horizontal_Distance_To_Fire_Points,…
  814683,3135,92,33,356,77,1450,229,229,187,1611,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  1357371,3052,99,20,337,207,625,195,191,9,2293,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  ```
- `train.csv` — 3600001 rows; first lines:
  ```
  Id,Elevation,Aspect,Slope,Horizontal_Distance_To_Hydrology,Vertical_Distance_To_Hydrology,Horizontal_Distance_To_Roadways,Hillshade_9am,Hillshade_Noon,Hillshade_3pm,Horizontal_Distance_To_Fire_Points,…
  3440475,2634,132,3,166,38,1247,251,210,119,3597,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2
  2470812,2769,89,5,633,10,626,177,209,178,-12,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2
  ```

## tabular-playground-series-may-2022
Tables:
- `sample_submission.csv` — 100001 rows; first lines:
  ```
  id,target
  800000,0.5
  800001,0.5
  ```
- `test.csv` — 100001 rows; first lines:
  ```
  id,f_00,f_01,f_02,f_03,f_04,f_05,f_06,f_07,f_08,f_09,f_10,f_11,f_12,f_13,f_14,f_15,f_16,f_17,f_18,f_19,f_20,f_21,f_22,f_23,f_24,f_25,f_26,f_27,f_28,f_29,f_30
  800000,0.1944912018912512,1.1809257689158985,-1.4745698238397122,-1.9699786768331715,-0.6322242017974853,-0.908536553676396,-0.9294142783609558,3,0,2,1,1,3,4,4,3,4,1,1,2.111812827602727,0.367227992823…
  800001,0.0735117261702696,1.215182024126669,1.887182790222917,0.6640998767720103,1.4459160587911233,0.4071437174007382,-0.9654628420274068,1,0,2,1,1,4,3,1,3,1,5,1,-0.8923782436311598,0.044842609615179…
  ```
- `train.csv` — 800001 rows; first lines:
  ```
  id,f_00,f_01,f_02,f_03,f_04,f_05,f_06,f_07,f_08,f_09,f_10,f_11,f_12,f_13,f_14,f_15,f_16,f_17,f_18,f_19,f_20,f_21,f_22,f_23,f_24,f_25,f_26,f_27,f_28,f_29,f_30,target
  0,-0.249088480127198,0.5306415748448242,0.3352271666250545,0.8068193746089833,-0.1841904948777198,-0.5604420211992777,1.2537666397727585,2,1,1,0,2,6,0,1,1,3,2,1,0.2275876887073882,0.7360906566723264,3…
  1,-0.312832922727397,0.0330816597210825,-0.5711931387274104,1.3114937880364494,0.9917182861837608,-0.1382494980384291,1.8346269755915832,2,1,2,2,1,1,2,2,4,3,0,3,2.045126957426498,-6.621720910819618,2.…
  ```

## tensorflow-speech-recognition-challenge
Tables:
- `sample_submission.csv` — 6474 rows; first lines:
  ```
  fname,label
  clip_00000000.wav,silence
  clip_00000001.wav,silence
  ```
Folders:
- `test/` — 0 files, 1 subfolders; examples: audio/clip_00003155.wav
- `train/` — 0 files, 1 subfolders; examples: audio/tree

## tensorflow2-question-answering
Tables:
- `sample_submission.csv` — 61477 rows; first lines:
  ```
  example_id,PredictionString
  -257485578111885185_short,
  -257485578111885185_long,
  ```
- `simplified-nq-test.jsonl` — 30738 rows; first lines:
  ```
  {"example_id":"-257485578111885185","question_text":"though the mills of god grind slowly yet they grind exceeding small","document_text":"Mills of God - wikipedia <H1> Mills of God <\/H1> Jump to : n…
  {"example_id":"-9110190923673509457","question_text":"what is the blind spot of the eye","document_text":"Blind spot ( vision ) - wikipedia <H1> Blind spot ( vision ) <\/H1> Jump to : navigation , sea…
  {"example_id":"-2606047177489670354","question_text":"the 3rd amendment prohibition on forced boarding of soldiers","document_text":"Third Amendment to the United States Constitution - wikipedia <H1> …
  ```
- `simplified-nq-train.jsonl` — 276635 rows; first lines:
  ```
  {"document_text":"Dale Dickey - wikipedia <H1> Dale Dickey <\/H1> <Table> <Tr> <Th_colspan=\"2\"> Dale Dickey <\/Th> <\/Tr> <Tr> <Th> <\/Th> <Td> Diana Dale Dickey ( 1961 - 09 - 29 ) September 29 , 19…
  {"document_text":"Old City ( Jerusalem ) - wikipedia <H1> Old City ( Jerusalem ) <\/H1> Jump to : navigation , search `` The template Infobox UNESCO World Heritage Site is being considered for deletio…
  {"document_text":"List of WWE champions - wikipedia <H1> List of WWE champions <\/H1> This article is about a list of wrestlers who have held the current WWE Championship . For a list of wrestlers who…
  ```

## text-normalization-challenge-english-language
Tables:
- `en_sample_submission_2.csv (inside en_sample_submission_2.csv.zip)` — 993466 rows; first lines:
  ```
  "id","after"
  "0_0","Rocky"
  "0_1","Mountain"
  ```
- `en_test_2.csv (inside en_test_2.csv.zip)` — 993466 rows; first lines:
  ```
  "sentence_id","token_id","before"
  0,0,"Rocky"
  0,1,"Mountain"
  ```
- `en_train.csv (inside en_train.csv.zip)` — 8924977 rows; first lines:
  ```
  "sentence_id","token_id","class","before","after"
  0,0,"PLAIN","Brillantaisia","Brillantaisia"
  0,1,"PLAIN","is","is"
  ```
Compressed artifacts:
- `en_sample_submission_2.csv.zip` [compressed] (entries: 1) — first entries: en_sample_submission_2.csv
- `en_test_2.csv.zip` [compressed] (entries: 1) — first entries: en_test_2.csv
- `en_train.csv.zip` [compressed] (entries: 1) — first entries: en_train.csv

## text-normalization-challenge-russian-language
Tables:
- `ru_sample_submission_2.csv (inside ru_sample_submission_2.csv.zip)` — 1059192 rows; first lines:
  ```
  "id","after"
  "0_0","Теперь"
  "0_1","все"
  ```
- `ru_test_2.csv (inside ru_test_2.csv.zip)` — 1059192 rows; first lines:
  ```
  "sentence_id","token_id","before"
  0,0,"Теперь"
  0,1,"все"
  ```
- `ru_train.csv (inside ru_train.csv.zip)` — 9515326 rows; first lines:
  ```
  "sentence_id","token_id","class","before","after"
  0,0,"PLAIN","По","По"
  0,1,"PLAIN","состоянию","состоянию"
  ```
Compressed artifacts:
- `ru_sample_submission_2.csv.zip` [compressed] (entries: 1) — first entries: ru_sample_submission_2.csv
- `ru_test_2.csv.zip` [compressed] (entries: 1) — first entries: ru_test_2.csv
- `ru_train.csv.zip` [compressed] (entries: 1) — first entries: ru_train.csv

## tgs-salt-identification-challenge
Tables:
- `depths.csv` — 3001 rows; first lines:
  ```
  id,z
  000e218f21,841
  00441f1cf2,330
  ```
- `sample_submission.csv` — 1001 rows; first lines:
  ```
  id,rle_mask
  003c477d7c,1 1
  0108518d1e,1 1
  ```
- `train.csv` — 3001 rows; first lines:
  ```
  id,rle_mask
  000e218f21,
  00441f1cf2,
  ```
Folders:
- `test/` — 0 files, 1 subfolders; examples: images/12bf4f2d3b.png
- `train/` — 0 files, 2 subfolders; examples: images/25dc959ebd.png, masks/25dc959ebd.png

## the-icml-2013-whale-challenge-right-whale-redux
Tables:
- `sampleSubmission.csv` — 25150 rows; first lines:
  ```
  clip,probability
  20090330_000000_015s2ms_Test0.aif,0
  20090330_000000_020s0ms_Test1.aif,0
  ```
Compressed artifacts:
- `test2.zip` [compressed] (entries: 25150) — first entries: test2/, test2/20090331_174500_64247s3ms_Test20854.aif, test2/20090330_223000_81608s2ms_Test10106.aif, test2/20090330_080000_28926s1ms_Test3105.aif, test2/20090331_004500_3463s2ms_Test11903.aif
- `train2.zip` [compressed] (entries: 22693) — first entries: train2/, train2/20090329_221500_80931s1ms_TRAIN22033_0.aif, train2/20090328_164500_61189s4ms_TRAIN4993_0.aif, train2/20090329_190000_68618s2ms_TRAIN20038_0.aif, train2/20090328_224500_82729s7ms_TRAIN7789_0.aif

## tweet-sentiment-extraction
Tables:
- `sample_submission.csv` — 2750 rows; first lines:
  ```
  textID,selected_text
  80a1e6bc32,
  863097735d,
  ```
- `test.csv` — 2750 rows; first lines:
  ```
  textID,text,sentiment
  80a1e6bc32,I just saw a shooting star... I made my wish,positive
  863097735d,gosh today sucks! i didnt get my tax returns! im so upset cuz now i have to miss my best friends wedding in washington...lame,negative
  ```
- `train.csv` — 24733 rows; first lines:
  ```
  textID,text,selected_text,sentiment
  8d4ad58b45,eating breakfast  getting ready to go to school ;(,eating breakfast  getting ready to go to school ;(,negative
  fdfe12a800,Going to fold laundry and then hit the sack. I have boring saturday evenings,I have boring saturday evenings,negative
  ```

## us-patent-phrase-to-phrase-matching
Tables:
- `sample_submission.csv` — 3649 rows; first lines:
  ```
  id,score
  2a988c7d98568627,0
  75a3ae03b26e2f7e,0
  ```
- `test.csv` — 3649 rows; first lines:
  ```
  id,anchor,target,context
  2a988c7d98568627,project onto surface,disposing,G03
  75a3ae03b26e2f7e,rotate on its longitudinal axis,gear grinding device,B24
  ```
- `train.csv` — 32826 rows; first lines:
  ```
  id,anchor,target,context,score
  378b8322a01b88db,obstacle course,obstacle position trajectory,B60,0.5
  f43c824b3d939294,hardware blocks,housing,G06,0.25
  ```

## uw-madison-gi-tract-image-segmentation
Tables:
- `sample_submission.csv` — 20401 rows; first lines:
  ```
  id,class,predicted
  case123_day20_slice_0001,large_bowel,1 1 5 2
  case123_day20_slice_0001,small_bowel,1 1 5 2
  ```
- `test.csv` — 20401 rows; first lines:
  ```
  id,class
  case123_day20_slice_0001,large_bowel
  case123_day20_slice_0001,small_bowel
  ```
- `train.csv` — 95089 rows; first lines:
  ```
  id,class,segmentation
  case77_day20_slice_0001,large_bowel,
  case77_day20_slice_0001,small_bowel,
  ```
Folders:
- `test/` — 0 files, 28 subfolders; examples: case119/case119_day25, case53/case53_day0, case131/case131_day23
- `train/` — 0 files, 76 subfolders; examples: case111/case111_day19, case119/case119_day20, case30/case30_day1

## ventilator-pressure-prediction
Tables:
- `sample_submission.csv` — 603601 rows; first lines:
  ```
  id,pressure
  1,0
  2,0
  ```
- `test.csv` — 603601 rows; first lines:
  ```
  id,breath_id,R,C,time_step,u_in,u_out
  1,44398,50,20,0,0.1338052724,0
  2,44398,50,20,0.03195524216,2.411108364,0
  ```
- `train.csv` — 5432401 rows; first lines:
  ```
  id,breath_id,R,C,time_step,u_in,u_out,pressure
  1,85053,5,10,0,4.174419212,0,6.118700287
  2,85053,5,10,0.03381204605,7.050149003,0,5.907793851
  ```

## vesuvius-challenge-ink-detection
Tables:
- `sample_submission.csv` — 2 rows; first lines:
  ```
  Id,Predicted
  a,1 1 5 1
  ```
Folders:
- `test/` — 0 files, 1 subfolders; examples: a/surface_volume
- `train/` — 0 files, 2 subfolders; examples: 1/ir.png, 2/ir.png

## vinbigdata-chest-xray-abnormalities-detection
Tables:
- `sample_submission.csv` — 1501 rows; first lines:
  ```
  image_id,PredictionString
  24b3c4ccc0e19044935c8f40ab37fc18,14 1 0 0 1 1
  295add70002001e13d65c0d0d4a100a0,14 1 0 0 1 1
  ```
- `train.csv` — 61172 rows; first lines:
  ```
  image_id,class_name,class_id,rad_id,x_min,y_min,x_max,y_max
  50a418190bc3fb1ef1633bf9678929b3,No finding,14,R11,,,,
  21a10246a5ec7af151081d0cd6d65dc9,No finding,14,R7,,,,
  ```
Folders:
- `test/` — 1500 files, 0 subfolders; examples: 64745dd6d13744f622c269f3a8e07721.dicom, ab659f1080296ba99ca110763beb2f72.dicom, 53d4fbf11ca8be107a343df37ca9eddc.dicom
- `train/` — 13500 files, 0 subfolders; examples: 18cf33473f5d32b6af44413f43b535a1.dicom, 81492bf07f022ecc16aa7b553948d4bb.dicom, 0302ee5d111875b1ed05dd6630404c6d.dicom

## whale-categorization-playground
Tables:
- `sample_submission.csv` — 2611 rows; first lines:
  ```
  Image,Id
  00087b01.jpg,new_whale w_1287fbc w_98baff9 w_7554f44 w_1eafe46
  0014cfdf.jpg,new_whale w_1287fbc w_98baff9 w_7554f44 w_1eafe46
  ```
- `train.csv` — 7241 rows; first lines:
  ```
  Image,Id
  00022e1a.jpg,w_e15442c
  000466c4.jpg,w_1287fbc
  ```
Folders:
- `test/` — 2610 files, 0 subfolders; examples: c37f74c6.jpg, ce8509c7.jpg, 40e1012f.jpg
- `train/` — 7240 files, 0 subfolders; examples: 0a3dbc55.jpg, 8cd881fb.jpg, 3db2b3b3.jpg
