
# Assessing autoregulation using cerebral oximetry in a prehospital setting

This project is an attempt to examine cerebral autoregulation using data recorded in a prehospital environment.

The two physiological signals used in this analysis are invasive blood pressure recorded using a ZOLL monitor-defibrillator, and left frontal lobe rSO<sub>2</sub> recorded each second using a Nonin H500 NIRS monitoring device. Data collection was done as a part of the [BOPRA study](https://boprastudy.fi) by Finnish HEMS physicians during patient transport under anaesthesia.

rSO<sub>2</sub>-MAP plots will be rendered to see if a pattern of the Lassen autoregulation curve emerges in measurement data recorded in a prehospital environment. The value of COx index will be plotted over time, and the time spent above the threshold COx > 0.3 will be noted to assess association with mortality, morbidity and quality of life. Also, COx-MAP plots will be rendered to see if a U-shaped curve emerges, revealing a supposed individualized optimal MAP for cerebral perfusion. With sufficient pressure variation, it should be possible to detect LLA/ULA at some degree of reliability.

Expected challenges are the relatively short duration of patient contact resulting in a scarce number of data points, as well as the mobile recording environment with plenty of interference.

The author of this analysis has no knowledge of the underlying pathologies or other patient metadata. This information exists in the BOPRA database and can be associated with each patient case for further research.

The purpose of this document is to facilitate the assessment of methodological validity. __For interpretation, please see__ [section 8](analysis.php?page=8_images) __for key visualizations of each case and__ [section 9](#step9) __for numerical statistics and whole-cohort charts.__ To assess the technical validity of this analysis, please refer to the source code at <https://github.com/makes/bopra>.

1. [Waveform Identification](#step1)
2. [Data Aggregation](#step2)
3. [Data Cleansing](#step3)
4. [Automatic Time Synchronization](#step4)
5. [Manual Time Synchronization](#step5)
6. [COx Index Over Time](#step6)
7. [COx vs MAP](#step7)
8. [Summary](#step8)
9. [Statistics](#step9)

## 1: Waveform Identification <a name="step1"></a>

The ZOLL monitor-defibrillator stores the physiological signals recorded under six channel ids (0 to 5). The purpose of this step is to identify the nature of each signal to ensure correct processing.

Two visualizations were created for each channel. The first one shows the entire time span of the signal, and the second one shows a zoomed-in detail of ten seconds at the fifteen minute mark.

[View the images used for signal identification](analysis.php?page=1_images)

### ___Hypothesis:___

Each signal can be assumed to occupy the same channel id predictably across all cases. The invasive arterial pressure waveform required for the analysis can be found in all twelve cases.

### ___Interpretation:___

Signals identified for each case:

![](waveforms_found_small.jpg)

### ___Conclusion:___

Cases 4, 11, 12, 14, 23, 27, 28, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 50, 52 and 57 did not contain the required IAP waveform, and thus will be excluded from further analysis.

Case 31 produces an unresolved loading error and will be excluded for the time being.

Cases 22, 30, 43, 44, 53 and 56 fail this step due to a software bug, but contain IAP data.

Of the 58 datasets provided, 37 have IAP data available under channel 1. Sample rate of the IAP pulse waveform is 125 Hz.

## 2: Data Aggregation <a name="step2"></a>

In this step, mean arterial pressure is computed from the pulse waveform using a moving average of 10 seconds, then resampled to match the 1 Hz sample rate of the rSO<sub>2</sub> signal.

A csv file containing both signals will be produced for each case, as well as a visualization of both signals on a common time axis.

The csv file will also contain columns indicating bad sample quality reported by the device, and a `Mark` field indicating start of anaesthesia.

### ___Hypothesis:___

Data from the two separate source devices can be converted to a common sample rate of 1 Hz and aggregated into a single csv file.

### ___Data:___

[View the visualizations](analysis.php?page=2_images)

### ___Conclusion:___

CSV files useful for further analysis were produced.

## 3: Data Cleansing <a name="step3"></a>

In this step, anomalies and artefacts in MAP data will be identified by visual inspection of the signal. Any obviously invalid samples will be marked for exclusion.

Invalid values in rSO<sub>2</sub> data have already been marked by the researchers based on field notes and visual inspection. These markings will be incorporated from a separate file. Corrected `Mark` timestamps indicating start of anaesthesia will also be included from this file. The corrections are based on field notes.

A csv file containing the data from step 2, amended with markings described above, will be generated.

_MAP datapoint exclusion criteria_:

Any MAP values not already marked as invalid by the monitoring device, where one or more of the following apply:

- Fluctuations at the start of IAP monitoring
- Sudden MAP surge above 180 mmHg AND immediate return to baseline recorded before the spike
- Sudden MAP drop below 40 mmHg, as would happen during arterial line flushing
- Periodically occurring MAP drop due to NIBP measurement

### ___Hypothesis:___

There will be artefacts in the blood pressure signal caused by movement and nursing procedures.

### ___Interpretation:___

- Blood pressure data manually marked for exclusion is shaded red.
- Blood pressure data automatically marked as low quality is shaded darker red/grey
- rSO<sub>2</sub> data manually marked for exclusion is shaded purple.
- rSO<sub>2</sub> data automatically marked as low quality is shaded blue.

![](images/3_00001_01.png)

[View all images](analysis.php?page=3_images)

### ___Conclusion:___

Case 24 was excluded from further analysis, as the rSO<sub>2</sub> signal was missing most of the time. Case 47 was excluded from further analysis, as no IAP data was recorded.

- Any abnormally high or abnormally low MAP readings were marked for exclusion.
- Periodically occurring drops in blood pressure were identified as a NIBP cuff restricting blood flow to the limb used for invasive blood pressure measurement. These values were marked for exclusion.
- The exclusion criteria are pending domain expert review.

A csv file containing the data described above was generated.

## 4: Automatic Synchronization <a name="step4"></a>

It has been noted that the two monitoring devices used for data collection may have a clock discrepancy of several minutes. This is identified as a potential source of error, as the vasogenic phenomena under analysis cycle within 20 to 180 seconds ([_Steiner et al. 2008_](https://doi.org/10.1007/s12028-008-9140-5)).

### ___Hypothesis:___

Automatic synchronization using cross-correlation can be used to reliably align the signals.

__Caveat:__ _Lack of_ correlation between the signals indicates good autoregulation.

### ___Interpretation:___

Here is an example auto-align attempt:

[View all images](analysis.php?page=4_images)

![](images/4_00006_01.png)
![](images/4_00006_02.png)
![](images/4_00006_03.png)
![](images/4_00006_04.png)
Effect of alignment on the MAP-rSO<sub>2</sub> pattern.

[View all images](analysis.php?page=4_images)

### ___Conclusion:___

Cross correlation produced sensible results in only part of the cases. The method is not suitable for this analysis.

## 5: Manual Synchronization <a name="step5"></a>

As the automatic cross-correlation method proved unreliable for aligning this type of data, time synchronization is done manually, by visual inspection.

### ___Hypothesis:___

Manual synchronization using visual inspection can be used to reliably align the signals.

### ___Interpretation:___

[View all images](analysis.php?page=5_images)

![](images/5_00006_01.png)
![](images/5_00006_02.png)
![](images/5_00006_03.png)
Effect of alignment on the MAP-rSO<sub>2</sub> pattern.

[View all images](analysis.php?page=5_images)

### ___Conclusion:___

Manual alignment was used, based on visual inspection of common patterns between the signals. Part of the cases show no clearly identifiable point of alignment.

<!-- ![](scatterplot_quality_small.jpg) -->

## 6. COx index over time <a name="step6"></a>

For BOPRA objective _"To assess the association between time on cerebral blood flow autoregulation range (defined as COx < 0.3) and mortality, morbidity and quality of life."_

Data discontinuities will be imputed using linear interpolation.

### ___Hypothesis:___

The COx index can be defined for a significant duration.

### ___Interpretation:___

[View all images](analysis.php?page=6_images)

![](images/6_00003_01.png)
![](images/6_00003_02.png)

[View all images](analysis.php?page=6_images)

### ___Conclusion:___

In most cases, there is sufficient overlap of MAP and rSO<sub>2</sub> to define COx.

## 7. COx vs MAP <a name="step7"></a>

### ___Hypothesis:___

Plotting COx over MAP, we should see a u-shaped curve, whose minimum represents optimal MAP target for autoregulation.

### ___Interpretation:___

[View all images](analysis.php?page=7_images)

![](images/7_00007_03.png)
![](images/7_00007_02.png)
![](images/7_00005_03.png)
![](images/7_00005_02.png)

[View all images](analysis.php?page=7_images)

### ___Conclusion:___

Some figures display a u-shaped or descending curve. Violin plots were generated to see where the most of the samples fall. This helps assess the actual blood pressure variation and to detect outliers. Expert physician interpretation is required to assess the results.

## 8: Summary <a name="step8"></a>

A selection of images from the previous steps were collected together. A scatterplot with marginal distributions and a fixed MAP axis was generated.

[View case summaries](analysis.php?page=8_images)

<!--
![](images/8_00007_05.png)
![](images/7_00007_02.png)

[View summary](analysis.php?page=8_images)
-->

## 9: Statistics <a name="step9"></a>

Cohort chart and some numerical statistics were generated.

[View Jupyter notebook](stats.html)

![](images/9_00000_04.png)

The cohort chart displays some kind of U-shape.

![](images/9_00000_01.png)

### Per-case statistics

Click the links in "Case ID" column to view case images.

|                                 Case ID |   COx > 0.3 |   COx SD |   COx defined |   COx mean |   COx median | Duration   |   MAP SD |   MAP mean |   MAP median |   rSO2 SD |   rSO2 mean |   rSO2 median |
|----------------------------------------:|------------:|---------:|--------------:|-----------:|-------------:|:-----------|---------:|-----------:|-------------:|----------:|------------:|--------------:|
|   [1](analysis.php?page=8_images#case1) |        0.36 |     0.42 |          0.85 |       0.09 |         0.02 | 01:09:13   |    23.92 |     112.08 |       104.26 |      6.25 |       85.28 |            85 |
|   [2](analysis.php?page=8_images#case2) |        0.61 |     0.5  |          0.7  |       0.39 |         0.5  | 00:50:55   |    25.67 |     119.87 |       112.65 |      3.49 |       68.39 |            69 |
|   [3](analysis.php?page=8_images#case3) |        0.45 |     0.53 |          0.58 |       0.18 |         0.21 | 01:38:33   |    19.99 |      88.44 |        81.41 |      7.11 |       75.59 |            72 |
|   [5](analysis.php?page=8_images#case5) |        0.3  |     0.49 |          0.49 |      -0.06 |        -0.07 | 01:25:34   |     7.43 |      91.86 |        90.61 |      5.61 |       67.96 |            65 |
|   [6](analysis.php?page=8_images#case6) |        0.54 |     0.34 |          0.62 |       0.37 |         0.37 | 01:20:43   |    20.33 |     103.89 |        93.43 |      4.32 |       94.97 |            96 |
|   [7](analysis.php?page=8_images#case7) |        0.4  |     0.38 |          0.56 |       0.24 |         0.17 | 01:18:24   |    10.65 |      97.14 |        95.57 |      3.56 |       83.97 |            84 |
|   [8](analysis.php?page=8_images#case8) |        0.44 |     0.48 |          0.75 |       0.09 |         0.14 | 01:04:03   |    17.55 |      92.63 |        88.06 |      1.27 |       90.13 |            90 |
|   [9](analysis.php?page=8_images#case9) |        0.58 |     0.51 |          0.48 |       0.3  |         0.47 | 00:45:49   |    24.79 |      96.47 |        88.12 |      2.31 |       63.07 |            63 |
| [10](analysis.php?page=8_images#case10) |        0.25 |     0.35 |          0.73 |       0.06 |         0.13 | 01:38:30   |     4.11 |      68.43 |        68.12 |      5.35 |       66.52 |            64 |
| [13](analysis.php?page=8_images#case13) |        0.21 |     0.4  |          0.62 |      -0    |        -0.02 | 01:23:50   |     6.26 |     105.75 |       105.13 |      1.03 |       81.52 |            81 |
| [15](analysis.php?page=8_images#case15) |        0.14 |     0.42 |          0.32 |      -0.09 |        -0.09 | 00:42:18   |     7.02 |      75.96 |        76.93 |      7.28 |       62.1  |            58 |
| [16](analysis.php?page=8_images#case16) |        0.29 |     0.44 |          0.35 |       0.11 |        -0.02 | 01:22:54   |    16.52 |      84.81 |        80.86 |      2.44 |       82.89 |            83 |
| [17](analysis.php?page=8_images#case17) |        0.41 |     0.49 |          0.48 |       0.23 |         0.24 | 00:52:45   |     5.45 |      69.98 |        68.4  |      5.54 |       51.52 |            49 |
| [18](analysis.php?page=8_images#case18) |        0    |     0.28 |          0.06 |      -0.44 |        -0.48 | 00:56:50   |    16.79 |      83.39 |        83.39 |      1.43 |       84.33 |            84 |
| [19](analysis.php?page=8_images#case19) |        0.5  |     0.41 |          0.62 |       0.32 |         0.3  | 01:24:41   |    13.32 |      97.6  |        99.5  |     11.77 |       66.97 |            70 |
| [20](analysis.php?page=8_images#case20) |        0.55 |     0.41 |          0.74 |       0.33 |         0.37 | 01:03:52   |    17.91 |     115.54 |       110.97 |      4.11 |       83.49 |            82 |
| [21](analysis.php?page=8_images#case21) |        0.21 |     0.34 |          0.49 |       0.04 |        -0.05 | 01:05:27   |     4.87 |     103.97 |       102.88 |      2.02 |       84.97 |            85 |
| [22](analysis.php?page=8_images#case22) |        0.48 |     0.52 |          0.42 |       0.27 |         0.24 | 01:03:38   |    57.77 |     192.38 |       221.92 |      4.15 |       62.62 |            63 |
| [25](analysis.php?page=8_images#case25) |        0.45 |     0.43 |          0.74 |       0.21 |         0.26 | 01:25:27   |    11.45 |     101.81 |       103.48 |      3.51 |       81.59 |            81 |
| [26](analysis.php?page=8_images#case26) |        0.43 |     0.51 |          0.53 |       0.18 |         0.18 | 01:28:21   |    36.38 |     121.49 |       121.25 |      2.52 |       72.91 |            73 |
| [29](analysis.php?page=8_images#case29) |        0.45 |     0.56 |          0.75 |       0.15 |         0.01 | 02:20:29   |    14.19 |     101.68 |        99.48 |      5.41 |       67.77 |            66 |
| [30](analysis.php?page=8_images#case30) |        0.14 |     0.27 |          0.27 |      -0.04 |        -0.09 | 01:11:09   |     8.85 |      87.66 |        85.78 |      2.18 |       89.74 |            90 |
| [41](analysis.php?page=8_images#case41) |        0.55 |     0.36 |          0.75 |       0.37 |         0.38 | 01:33:19   |    21.34 |      86.48 |        89.99 |      2.2  |       77.14 |            78 |
| [42](analysis.php?page=8_images#case42) |        0.8  |     0.43 |          0.54 |       0.53 |         0.69 | 01:02:46   |    13.83 |     129.55 |       126.82 |      3.26 |       79.47 |            79 |
| [43](analysis.php?page=8_images#case43) |        0.09 |     0.4  |          0.52 |      -0.31 |        -0.37 | 00:40:55   |     9.2  |      76.81 |        76.54 |      2.41 |       78.24 |            77 |
| [44](analysis.php?page=8_images#case44) |        0.36 |     0.32 |          0.82 |       0.16 |         0.15 | 01:30:08   |     7.13 |      89.17 |        88.2  |      1.92 |       72.8  |            73 |
| [45](analysis.php?page=8_images#case45) |        0.52 |     0.43 |          0.72 |       0.23 |         0.34 | 00:57:29   |    13.8  |     105.24 |       102.74 |      2.76 |       88.15 |            89 |
| [46](analysis.php?page=8_images#case46) |        0.23 |     0.53 |          0.63 |      -0.2  |        -0.3  | 01:08:43   |    11.56 |     116.45 |       113.53 |      6.64 |       74.41 |            72 |
| [49](analysis.php?page=8_images#case49) |        0.84 |     0.47 |          0.52 |       0.65 |         0.84 | 01:15:48   |    16.75 |      72.22 |        75.44 |      9.65 |       62.39 |            67 |
| [51](analysis.php?page=8_images#case51) |        0.65 |     0.57 |          0.5  |       0.37 |         0.56 | 01:14:00   |    11.88 |      46.5  |        45.4  |      5.18 |       85.34 |            83 |
| [53](analysis.php?page=8_images#case53) |        0.91 |     0.25 |          0.53 |       0.71 |         0.79 | 01:01:22   |    12.18 |      71.12 |        69.6  |      3.11 |       62.57 |            63 |
| [54](analysis.php?page=8_images#case54) |        0.12 |     0.38 |          0.37 |      -0.13 |        -0.09 | 01:17:26   |    21.32 |     135.77 |       129.46 |      3.13 |       80.75 |            80 |
| [55](analysis.php?page=8_images#case55) |        0.34 |     0.47 |          0.59 |       0.06 |         0.02 | 01:20:58   |    14.09 |     106.58 |       100.25 |      3.93 |       93.38 |            94 |
| [58](analysis.php?page=8_images#case58) |        0.5  |     0.42 |          0.42 |       0.26 |         0.29 | 02:19:41   |    11.15 |      92.86 |        93.39 |      5.79 |       75.12 |            72 |

### Whole-cohort statistics

Histograms showing the distributions:

![](images/9_00000_05.png)

    COx:  mean 0.19   median 0.20   sd 0.48
    MAP:  mean 97.04  median 95.74  sd 27.84
    rSO2: mean 75.54  median 75.74  sd 10.45
    COx:  mean 0.19   median 0.20   sd 0.48

![](images/9_00000_02.png)

[View Jupyter notebook](stats.html)