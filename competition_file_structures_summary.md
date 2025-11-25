# Competition File Structure Summary

This document summarizes the layout of each competition, which the grader mounts under `./data`. Each section lists representative files and folders; compressed assets are annotated with `[compressed]`. The `./data` directory is read-only, so these assets can only be accessed after decompressing them elsewhere within the working directory `.`.

## 3d-object-detection-for-autonomous-vehicles
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test_data/ — files: 11 (.json×11); e.g., attribute.json, calibrated_sensor.json, category.json … (+8 more)
- test_images/ — files: 31752 (.jpeg×31752); e.g., host-a004_cam0_1232815252251064006.jpeg, host-a004_cam0_1232815252451064006.jpeg, host-a004_cam0_1232815252651064006.jpeg … (+31749 more)
- test_lidar/ — files: 5544 (.bin×5544); e.g., host-a004_lidar1_1232815252301696606.bin, host-a004_lidar1_1232815252501972246.bin, host-a004_lidar1_1232815252701880486.bin … (+5541 more)
- test_maps/ — files: 1 (.png×1); e.g., map_raster_palo_alto.png
- train_data/ — files: 13 (.json×13); e.g., attribute.json, calibrated_sensor.json, category.json … (+10 more)
- train_images/ — files: 127005 (.jpeg×127005); e.g., host-a004_cam0_1232817645251064006.jpeg, host-a004_cam0_1232817645451064006.jpeg, host-a004_cam0_1232817645651064006.jpeg … (+127002 more)
- train_lidar/ — files: 25200 (.bin×25200); e.g., host-a004_lidar1_1232817645301209606.bin, host-a004_lidar1_1232817645501052246.bin, host-a004_lidar1_1232817645700948486.bin … (+25197 more)
- train_maps/ — files: 1 (.png×1); e.g., map_raster_palo_alto.png

## AI4Code
Root files (4): description.md, sample_submission.csv, train_ancestors.csv, train_orders.csv
Key folders:
- test/ — files: 20000 (.json×20000); e.g., 00015c83e2717b.json, 0001bdd4021779.json, 000757b90aaca0.json … (+19997 more)
- train/ — files: 119256 (.json×119256); e.g., 00001756c60be8.json, 0001daf4c2c76d.json, 0002115f48f982.json … (+119253 more)

## aerial-cactus-identification
Root files (5): description.md, sample_submission.csv, test.zip [compressed], train.csv, train.zip [compressed]
Key folders: none

## alaska2-image-steganalysis
Root files (2): description.md, sample_submission.csv
Key folders:
- Cover/ — files: 70000 (.jpg×70000); e.g., 00001.jpg, 00002.jpg, 00003.jpg … (+69997 more)
- JMiPOD/ — files: 70000 (.jpg×70000); e.g., 00001.jpg, 00002.jpg, 00003.jpg … (+69997 more)
- JUNIWARD/ — files: 70000 (.jpg×70000); e.g., 00001.jpg, 00002.jpg, 00003.jpg … (+69997 more)
- Test/ — files: 5000 (.jpg×5000); e.g., 0001.jpg, 0002.jpg, 0003.jpg … (+4997 more)
- UERD/ — files: 70000 (.jpg×70000); e.g., 00001.jpg, 00002.jpg, 00003.jpg … (+69997 more)

## aptos2019-blindness-detection
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test_images/ — files: 367 (.png×367); e.g., 001639a390f0.png, 01b3aed3ed4c.png, 0232dfea7547.png … (+364 more)
- train_images/ — files: 3295 (.png×3295); e.g., 000c1434d8d7.png, 0024cdab0c1e.png, 002c21358ce6.png … (+3292 more)

## billion-word-imputation
Root files (3): description.md, test_v2.txt.zip [compressed], train_v2.txt.zip [compressed]
Key folders: none

## bms-molecular-translation
Root files (4): description.md, extra_approved_InChIs.csv, sample_submission.csv, train_labels.csv
Key folders:
- test/ — files: none — subfolders: 16; e.g., 0/, 1/, 2/ … (+13 more)
- train/ — files: none — subfolders: 16; e.g., 0/, 1/, 2/ … (+13 more)

## cassava-leaf-disease-classification
Root files (4): description.md, label_num_to_disease_map.json, sample_submission.csv, train.csv
Key folders:
- test_images/ — files: 2676 (.jpg×2676); e.g., 1234294272.jpg, 1234332763.jpg, 1234375577.jpg … (+2673 more)
- test_tfrecords/ — files: 2 (.tfrec×2); e.g., ld_test00-1338.tfrec, ld_test01-1338.tfrec
- train_images/ — files: 18721 (.jpg×18721); e.g., 1000015157.jpg, 1000201771.jpg, 100042118.jpg … (+18718 more)
- train_tfrecords/ — files: 14 (.tfrec×14); e.g., ld_train00-1338.tfrec, ld_train01-1338.tfrec, ld_train02-1338.tfrec … (+11 more)

## cdiscount-image-classification-challenge
Root files (6): category_names.csv, description.md, sample_submission.csv, test.bson, train.bson, train_example.bson
Key folders: none

## chaii-hindi-and-tamil-question-answering
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## champs-scalar-coupling
Root files (10): description.md, dipole_moments.csv, magnetic_shielding_tensors.csv, mulliken_charges.csv, potential_energy.csv, sample_submission.csv, scalar_coupling_contributions.csv, structures.csv, test.csv, train.csv
Key folders:
- structures/ — files: 76510 (.xyz×76510); e.g., dsgdb9nsd_000001.xyz, dsgdb9nsd_000002.xyz, dsgdb9nsd_000003.xyz … (+76507 more)

## denoising-dirty-documents
Root files (2): description.md, sampleSubmission.csv
Key folders:
- test/ — files: 29 (.png×29); e.g., 110.png, 111.png, 122.png … (+26 more)
- train/ — files: 115 (.png×115); e.g., 101.png, 102.png, 104.png … (+112 more)
- train_cleaned/ — files: 115 (.png×115); e.g., 101.png, 102.png, 104.png … (+112 more)

## detecting-insults-in-social-commentary
Root files (4): description.md, sample_submission_null.csv, test.csv, train.csv
Key folders: none

## dog-breed-identification
Root files (3): description.md, labels.csv, sample_submission.csv
Key folders:
- test/ — files: 1023 (.jpg×1023); e.g., 0042188c895a2f14ef64a918ed9c7b64.jpg, 007ff9a78eba2aebb558afea3a51c469.jpg, 00cc68a50b2d016a6b29af628ea4e04b.jpg … (+1020 more)
- train/ — files: 9199 (.jpg×9199); e.g., 000bec180eb18c7604dcecc8fe0dba07.jpg, 001513dfcb2ffafc82cccf4d8bbaba97.jpg, 001cdf01b096e06d78e9e5112d419397.jpg … (+9196 more)

## dogs-vs-cats-redux-kernels-edition
Root files (4): description.md, sample_submission.csv, test.zip [compressed], train.zip [compressed]
Key folders:
- test/ — files: 2500 (.jpg×2500); e.g., 1.jpg, 10.jpg, 100.jpg … (+2497 more)
- train/ — files: 22500 (.0.jpg×2, .1.jpg×2, .10.jpg×2); e.g., cat.0.jpg, cat.1.jpg, cat.10.jpg … (+22497 more)

## facebook-recruiting-iii-keyword-extraction
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## freesound-audio-tagging-2019
Root files (7): description.md, sample_submission.csv, test.zip [compressed], train_curated.csv, train_curated.zip [compressed], train_noisy.csv, train_noisy.zip [compressed]
Key folders: none

## google-quest-challenge
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## google-research-identify-contrails-reduce-global-warming
Root files (4): description.md, sample_submission.csv, train_metadata.json, validation_metadata.json
Key folders:
- test/ — files: none — subfolders: 1856; e.g., 1006714073984511039/, 1011991214639847439/, 1017161294763190782/ … (+1853 more)
- train/ — files: none — subfolders: 18673; e.g., 1000216489776414077/, 1000603527582775543/, 1000660467359258186/ … (+18670 more)
- validation/ — files: none — subfolders: 1856; e.g., 1000834164244036115/, 1002653297254493116/, 1002777035567823518/ … (+1853 more)

## h-and-m-personalized-fashion-recommendations
Root files (5): articles.csv, customers.csv, description.md, sample_submission.csv, transactions_train.csv
Key folders:
- images/ — files: none — subfolders: 86; e.g., 010/, 011/, 012/ … (+83 more)

## herbarium-2020-fgvc7
Root files (2): description.md, sample_submission.csv
Key folders:
- nybg2020/ — files: none — subfolders: 2; e.g., test/, train/

## herbarium-2021-fgvc8
Root files (2): description.md, sample_submission.csv
Key folders:
- test/ — files: 1 (.json×1); e.g., metadata.json — subfolders: 1; e.g., images/
- train/ — files: 1 (.json×1); e.g., metadata.json — subfolders: 1; e.g., images/

## herbarium-2022-fgvc9
Root files (4): description.md, sample_submission.csv, test_metadata.json, train_metadata.json
Key folders:
- test_images/ — files: none — subfolders: 175; e.g., 000/, 001/, 002/ … (+172 more)
- train_images/ — files: none — subfolders: 156; e.g., 000/, 001/, 002/ … (+153 more)

## histopathologic-cancer-detection
Root files (3): description.md, sample_submission.csv, train_labels.csv
Key folders:
- test/ — files: 45561 (.tif×45561); e.g., 00004aab08381d25d315384d646f5ce413ea24b1.tif, 0000da768d06b879e5754c43e2298ce48726f722.tif, 00011545a495817817c6943583b294c900a137b8.tif … (+45558 more)
- train/ — files: 174464 (.tif×174464); e.g., 00001b2b5609af42ab0ab276dd4cd41c3e7745b5.tif, 000020de2aa6193f4c160e398a8edea95b1da598.tif, 0000d563d5cfafc4e68acb7c9829258a298d9b6a.tif … (+174461 more)

## hms-harmful-brain-activity-classification
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- example_figures/ — files: 20 (.pdf×20); e.g., Sample01.pdf, Sample02.pdf, Sample03.pdf … (+17 more)
- test_eegs/ — files: 1693 (.parquet×1693); e.g., 1001717358.parquet, 1003353736.parquet, 1004626343.parquet … (+1690 more)
- test_spectrograms/ — files: 1114 (.parquet×1114); e.g., 1002209002.parquet, 1005228554.parquet, 1006082535.parquet … (+1111 more)
- train_eegs/ — files: 15396 (.parquet×15396); e.g., 1000913311.parquet, 1001369401.parquet, 1001487592.parquet … (+15393 more)
- train_spectrograms/ — files: 10024 (.parquet×10024); e.g., 1000086677.parquet, 1000189855.parquet, 1000317312.parquet … (+10021 more)

## hotel-id-2021-fgvc8
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test_images/ — files: 9756 (.jpg×9756); e.g., 80196e6999ce63cf.jpg, 80296afd55d516ea.jpg, 802aab95d62b7daa.jpg … (+9753 more)
- train_images/ — files: none — subfolders: 88; e.g., 0/, 1/, 10/ … (+85 more)

## hubmap-kidney-segmentation
Root files (4): description.md, HuBMAP-20-dataset_information.csv, sample_submission.csv, train.csv
Key folders:
- test/ — files: 10 (.json×6, .tiff×3, .csv×1); e.g., 0486052bb-anatomical-structure.json, 0486052bb.json, 0486052bb.tiff … (+7 more)
- train/ — files: 36 (.json×24, .tiff×12); e.g., 1e2425f28-anatomical-structure.json, 1e2425f28.json, 1e2425f28.tiff … (+33 more)

## imet-2020-fgvc7
Root files (4): description.md, labels.csv, sample_submission.csv, train.csv
Key folders:
- test/ — files: 21318 (.png×21318); e.g., 00053412b382618eceb2ade4658c34a0.png, 00083381310738522bacb607cf5581fd.png, 000a29222fe555d01844c73012af16d6.png … (+21315 more)
- train/ — files: 120801 (.png×120801); e.g., 000040d66f14ced4cdd18cd95d91800f.png, 0000ef13e37ef70412166725ec034a8a.png, 0001eeb4a06e8daa7c6951bcd124c3c7.png … (+120798 more)

## inaturalist-2019-fgvc6
Root files (7): description.md, kaggle_sample_submission.csv, test2019.json, test2019.tar.gz [compressed], train2019.json, train_val2019.tar.gz [compressed], val2019.json
Key folders: none

## invasive-species-monitoring
Root files (5): description.md, sample_submission.csv.zip [compressed], test.7z [compressed], train.7z [compressed], train_labels.csv.zip [compressed]
Key folders: none

## iwildcam-2019-fgvc6
Root files (6): description.md, sample_submission.csv, test.csv, test_images.zip [compressed], train.csv, train_images.zip [compressed]
Key folders: none

## iwildcam-2020-fgvc7
Root files (5): description.md, iwildcam2020_megadetector_results.json, iwildcam2020_test_information.json, iwildcam2020_train_annotations.json, sample_submission.csv
Key folders:
- test/ — files: 60760 (.jpg×60760); e.g., 86760c00-21bc-11ea-a13a-137349068a90.jpg, 8676197a-21bc-11ea-a13a-137349068a90.jpg, 86762d0c-21bc-11ea-a13a-137349068a90.jpg … (+60757 more)
- train/ — files: 157199 (.jpg×157199); e.g., 86762118-21bc-11ea-a13a-137349068a90.jpg, 867630d6-21bc-11ea-a13a-137349068a90.jpg, 867634be-21bc-11ea-a13a-137349068a90.jpg … (+157196 more)

## jigsaw-toxic-comment-classification-challenge
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## jigsaw-unintended-bias-in-toxicity-classification
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## kuzushiji-recognition
Root files (6): description.md, sample_submission.csv, test_images.zip [compressed], train.csv, train_images.zip [compressed], unicode_translation.csv
Key folders: none

## leaf-classification
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- images/ — files: 990 (.jpg×990); e.g., 1.jpg, 10.jpg, 100.jpg … (+987 more)

## learning-agency-lab-automated-essay-scoring-2
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## lmsys-chatbot-arena
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## ml2021spring-hw2
Root files (2): description.md, sampleSubmission.csv
Key folders:
- timit_11/ — files: none — subfolders: 1; e.g., timit_11/

## mlsp-2013-birds
Root files (2): description.md, sample_submission.csv
Key folders:
- essential_data/ — files: 4 (.txt×4); e.g., CVfolds_2.txt, rec_id2filename.txt, rec_labels_test_hidden.txt … (+1 more) — subfolders: 1; e.g., src_wavs/
- supplemental_data/ — files: 5 (.txt×3, .bmp×2); e.g., histogram_of_segments.txt, segment_clusters.bmp, segment_features.txt … (+2 more) — subfolders: 4; e.g., filtered_spectrograms/, segmentation_examples/, spectrograms/ … (+1 more)

## movie-review-sentiment-analysis-kernels-only
Root files (4): description.md, sampleSubmission.csv, test.tsv.zip [compressed], train.tsv.zip [compressed]
Key folders: none

## multi-modal-gesture-recognition
Root files (14): description.md, devel01-40.7z [compressed], randomPredictions.csv, sample_code_mmrgc.zip [compressed], test.csv, test.tar.gz [compressed], training.csv, training1.tar.gz [compressed], training2.tar.gz [compressed], training3.tar.gz [compressed] … (+4 more)
Key folders: none

## new-york-city-taxi-fare-prediction
Root files (5): description.md, GCP-Coupons-Instructions.rtf, labels.csv, sample_submission.csv, test.csv
Key folders: none

## nfl-player-contact-detection
Root files (9): description.md, sample_submission.csv, test_baseline_helmets.csv, test_player_tracking.csv, test_video_metadata.csv, train_baseline_helmets.csv, train_labels.csv, train_player_tracking.csv, train_video_metadata.csv
Key folders:
- test/ — files: 72 (.mp4×72); e.g., 58187_001341_All29.mp4, 58187_001341_Endzone.mp4, 58187_001341_Sideline.mp4 … (+69 more)
- train/ — files: 648 (.mp4×648); e.g., 58168_003392_All29.mp4, 58168_003392_Endzone.mp4, 58168_003392_Sideline.mp4 … (+645 more)

## nomad2018-predict-transparent-conductors
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test/ — files: none — subfolders: 240; e.g., 1/, 10/, 100/ … (+237 more)
- train/ — files: none — subfolders: 2160; e.g., 1/, 10/, 100/ … (+2157 more)

## osic-pulmonary-fibrosis-progression
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test/ — files: none — subfolders: 18; e.g., ID00014637202177757139317/, ID00019637202178323708467/, ID00047637202184938901501/ … (+15 more)
- train/ — files: none — subfolders: 158; e.g., ID00007637202177411956430/, ID00009637202177434476278/, ID00010637202177584971671/ … (+155 more)

## paddy-disease-classification
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test_images/ — files: 2602 (.jpg×2602); e.g., 100011.jpg, 100012.jpg, 100015.jpg … (+2599 more)
- train_images/ — files: none — subfolders: 10; e.g., bacterial_leaf_blight/, bacterial_leaf_streak/, bacterial_panicle_blight/ … (+7 more)

## petfinder-pawpularity-score
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test/ — files: 992 (.jpg×992); e.g., 0049cb81313c94fa007286e9039af910.jpg, 0067aaaa500b530c76b9c91af34b4cb8.jpg, 0075ec6503412f21cf65ac5f43d80440.jpg … (+989 more)
- train/ — files: 8920 (.jpg×8920); e.g., 0007de18844b0dbbb5e1f607da0606e0.jpg, 0009c66b9439883ba2750fb825e1d7db.jpg, 0013fd999caf9a3efe1352ca1b0d937e.jpg … (+8917 more)

## plant-pathology-2020-fgvc7
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- images/ — files: 1821 (.jpg×1821); e.g., Test_0.jpg, Test_1.jpg, Test_10.jpg … (+1818 more)

## plant-pathology-2021-fgvc8
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test_images/ — files: 3727 (.jpg×3727); e.g., 801f78399a44e7af.jpg, 8023c3f31f875b6c.jpg, 802969daaddbbc8c.jpg … (+3724 more)
- train_images/ — files: 14905 (.jpg×14905); e.g., 800113bb65efe69e.jpg, 8002cb321f8bfcdf.jpg, 80070f7fb5e2ccaa.jpg … (+14902 more)

## plant-seedlings-classification
Root files (2): description.md, sample_submission.csv
Key folders:
- test/ — files: 666 (.png×666); e.g., 0012f11c4.png, 00268e97d.png, 006196e1c.png … (+663 more)
- train/ — files: none — subfolders: 12; e.g., Black-grass/, Charlock/, Cleavers/ … (+9 more)

## playground-series-s3e18
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## predict-volcanic-eruptions-ingv-oe
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test/ — files: 444 (.csv×444); e.g., 1003520023.csv, 1004346803.csv, 1007996426.csv … (+441 more)
- train/ — files: 3987 (.csv×3987); e.g., 1000015382.csv, 1000554676.csv, 1000745424.csv … (+3984 more)

## random-acts-of-pizza
Root files (6): description.md, sampleSubmission.csv, test.json, test.zip [compressed], train.json, train.zip [compressed]
Key folders: none

## ranzcr-clip-catheter-line-classification
Root files (4): description.md, sample_submission.csv, train.csv, train_annotations.csv
Key folders:
- test/ — files: 3009 (.2.826.0.1.3680043.8.498.10000428974990117276582711948006105617.jpg×1, .2.826.0.1.3680043.8.498.10009804582155067294620004418359998775.jpg×1, .2.826.0.1.3680043.8.498.10012868114746340015145674058758665450.jpg×1); e.g., 1.2.826.0.1.3680043.8.498.10000428974990117276582711948006105617.jpg, 1.2.826.0.1.3680043.8.498.10009804582155067294620004418359998775.jpg, 1.2.826.0.1.3680043.8.498.10012868114746340015145674058758665450.jpg … (+3006 more)
- train/ — files: 27074 (.2.826.0.1.3680043.8.498.10001065121843652267743449160233082683.jpg×1, .2.826.0.1.3680043.8.498.10001175380298620851477409998730672515.jpg×1, .2.826.0.1.3680043.8.498.10001274045312501651093242392099983211.jpg×1); e.g., 1.2.826.0.1.3680043.8.498.10001065121843652267743449160233082683.jpg, 1.2.826.0.1.3680043.8.498.10001175380298620851477409998730672515.jpg, 1.2.826.0.1.3680043.8.498.10001274045312501651093242392099983211.jpg … (+27071 more)

## rsna-2022-cervical-spine-fracture-detection
Root files (5): description.md, sample_submission.csv, test.csv, train_bounding_boxes.csv, train.csv
Key folders:
- segmentations/ — files: 9 (1.2.826.0.1.3680043.12292.nii, 1.2.826.0.1.3680043.24617.nii, etc.)
- train_images/1.2.826.0.1.3680043.21561 — files: 385 (1.dcm, 2.dcm, 3.dcm, etc.)

## rsna-breast-cancer-detection
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test_images/ — files: none — subfolders: 1192; e.g., 10116/, 10130/, 10188/ … (+1189 more)
- train_images/ — files: none — subfolders: 10721; e.g., 10006/, 10011/, 10025/ … (+10718 more)

## rsna-miccai-brain-tumor-radiogenomic-classification
Root files (3): description.md, sample_submission.csv, train_labels.csv
Key folders:
- test/ — files: none — subfolders: 59; e.g., 00002/, 00019/, 00021/ … (+56 more)
- train/ — files: none — subfolders: 526; e.g., 00000/, 00003/, 00005/ … (+523 more)

## seti-breakthrough-listen
Root files: description.md, sample_submission.csv, train_labels.csv
Key folders:
- test/ — `.npy` waterfall snapshots organized into numeric shards (`0/` … `9/`); e.g., 0/0016fd6c09d476d.npy, 0/0017643c1c5c254.npy
- train/ — `.npy` training windows with the same shard layout; e.g., 0/0000799a2b2c42d.npy, 0/00042890562ff68.npy
- old_leaky_data/ — holds `test_labels_old.csv`, `train_labels_old.csv`, plus `test_old/` and `train_old/` shard folders

## siim-covid19-detection
Root files (4): description.md, sample_submission.csv, train_image_level.csv, train_study_level.csv
Key folders:
- test/ — files: none — subfolders: 606; e.g., 000c9c05fd14/, 00c74279c5b7/, 00ccd633fb0e/ … (+603 more)
- train/ — files: none — subfolders: 5448; e.g., 00086460a852/, 00292f8c37bd/, 005057b3f880/ … (+5445 more)

## siim-isic-melanoma-classification
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- jpeg/ — files: none — subfolders: 2; e.g., test/, train/
- test/ — files: 4142 (.dcm×4142); e.g., ISIC_0052212.dcm, ISIC_0076545.dcm, ISIC_0085172.dcm … (+4139 more)
- tfrecords/ — files: 16 (.tfrec×16); e.g., test00-2071.tfrec, test01-2071.tfrec, train00-2071.tfrec … (+13 more)
- train/ — files: 28984 (.dcm×28984); e.g., ISIC_0015719.dcm, ISIC_0068279.dcm, ISIC_0074268.dcm … (+28981 more)

## smartphone-decimeter-2022
Root files (2): description.md, sample_submission.csv
Key folders:
- metadata/ — files: 3 (.json×2, .csv×1); e.g., accumulated_delta_range_state_bit_map.json, constellation_type_mapping.csv, raw_state_bit_map.json
- test/ — files: none — subfolders: 8; e.g., 2020-06-04-US-MTV-1/, 2020-06-04-US-MTV-2/, 2020-07-08-US-MTV-1/ … (+5 more)
- train/ — files: none — subfolders: 54; e.g., 2020-05-15-US-MTV-1/, 2020-05-21-US-MTV-1/, 2020-05-21-US-MTV-2/ … (+51 more)

## spaceship-titanic
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## spooky-author-identification
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## stanford-covid-vaccine
Root files (4): description.md, sample_submission.csv, test.json, train.json
Key folders: none

## statoil-iceberg-classifier-challenge
Root files (4): description.md, sample_submission.csv.7z [compressed], test.json.7z [compressed], train.json.7z [compressed]
Key folders: none

## tabular-playground-series-dec-2021
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## tabular-playground-series-may-2022
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## tensorflow-speech-recognition-challenge
Root files (2): description.md, sample_submission.csv
Key folders:
- test/ — files: none — subfolders: 1; e.g., audio/
- train/ — files: none — subfolders: 1; e.g., audio/

## tensorflow2-question-answering
Root files (4): description.md, sample_submission.csv, simplified-nq-test.jsonl, simplified-nq-train.jsonl
Key folders: none

## text-normalization-challenge-english-language
Root files (4): description.md, en_sample_submission_2.csv.zip [compressed], en_test_2.csv.zip [compressed], en_train.csv.zip [compressed]
Key folders: none

## text-normalization-challenge-russian-language
Root files (4): description.md, ru_sample_submission_2.csv.zip [compressed], ru_test_2.csv.zip [compressed], ru_train.csv.zip [compressed]
Key folders: none

## tgs-salt-identification-challenge
Root files (4): depths.csv, description.md, sample_submission.csv, train.csv
Key folders:
- test/ — files: none — subfolders: 1; e.g., images/
- train/ — files: none — subfolders: 2; e.g., images/, masks/

## the-icml-2013-whale-challenge-right-whale-redux
Root files (4): description.md, sampleSubmission.csv, test2.zip [compressed], train2.zip [compressed]
Key folders: none

## tweet-sentiment-extraction
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## us-patent-phrase-to-phrase-matching
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## uw-madison-gi-tract-image-segmentation
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders:
- test/ — files: none — subfolders: 28; e.g., case110/, case113/, case114/ … (+25 more)
- train/ — files: none — subfolders: 76; e.g., case101/, case102/, case107/ … (+73 more)

## ventilator-pressure-prediction
Root files (4): description.md, sample_submission.csv, test.csv, train.csv
Key folders: none

## vesuvius-challenge-ink-detection
Root files (2): description.md, sample_submission.csv
Key folders:
- test/ — files: none — subfolders: 1; e.g., a/
- train/ — files: none — subfolders: 2; e.g., 1/, 2/

## vinbigdata-chest-xray-abnormalities-detection
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test/ — files: 1500 (.dicom×1500); e.g., 00575e3846ebd05a909d97ba59c53d30.dicom, 0059d21bef1793fa9522e4ec8cae1a1a.dicom, 009fc6795a7be2faa76c6e1005edc418.dicom … (+1497 more)
- train/ — files: 13500 (.dicom×13500); e.g., 000434271f63a053c4128a0ba6352c7f.dicom, 00053190460d56c53cc3e57321387478.dicom, 0005e8e3701dfb1dd93d53e2ff537b6e.dicom … (+13497 more)

## whale-categorization-playground
Root files (3): description.md, sample_submission.csv, train.csv
Key folders:
- test/ — files: 2610 (.jpg×2610); e.g., 00087b01.jpg, 0014cfdf.jpg, 0035632e.jpg … (+2607 more)
- train/ — files: 7240 (.jpg×7240); e.g., 00022e1a.jpg, 000466c4.jpg, 001296d5.jpg … (+7237 more)
