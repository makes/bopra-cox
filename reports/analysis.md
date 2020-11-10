
# Assessing autoregulation using cerebral oximetry in a prehospital setting

The purpose of this analysis is to find out if a pattern of the Lassen autoregulation curve can be found in measurement data recorded in a prehospital environment.

The two physiological signals used in this analysis are invasive blood pressure recorded using a ZOLL monitor-defibrillator, and left frontal lobe rSO<sub>2</sub> recorded using a Nonin H500 NIRS monitoring device. Data collection was done as a part of the [BOPRA study](https://boprastudy.fi).

The source code can be found at <https://github.com/makes/bopra>.

1. [Waveform Identification](#step1)
2. [Data Aggregation](#step2)
3. [Data Cleansing](#step3)
4. [MAP-rSO<sub>2</sub> Scatterplot](#step4)
5. [Time Synchronization](#step5)
6. [Scatterplot Smoothing](#step6)
7. [COx Index Over Time](#step7)

## 1: Waveform Identification <a name="step1"></a>

The ZOLL monitor-defibrillator stores the physiological signals recorded under six channel ids (0 to 5). The purpose of this step is to identify the nature of each signal to ensure correct processing.

Two visualizations were created for each channel. The first one shows the entire time span of the signal, and the second one shows a zoomed-in detail of ten seconds at the fifteen minute mark.

[View the images used for signal identification](analysis.php?page=1_images)

### ___Hypothesis:___

Each signal can be assumed to occupy the same channel id predictably across all cases. The invasive arterial pressure waveform required for the analysis can be found in all twelve cases.

### ___Data:___

Signals identified for each case:

![](waveforms_found_small.jpg)

### ___Conclusion:___

Cases 4, 11, 12, 14, 23, 27, 28, 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 50, 52 and 57 did not contain the required IAP waveform, and thus will be excluded from further analysis.

Cases 22, 30, 31, 43, 44, 53 and 56 produce unresolved loading errors and will be excluded for the time being.

Of the 58 datasets provided, 31 have IAP data available under channel 1. Sample rate of the IAP pulse waveform is 125 Hz.

## 2: Data Aggregation <a name="step2"></a>

In this step, mean arterial pressure is computed from the pulse waveform using a moving average of 10 seconds, then resampled to match the 1 Hz sample rate of the rSO<sub>2</sub> signal.

A csv file containing both signals will be produced for each case, as well as a visualization of both signals on a common time axis.

The csv file will also contain columns indicating bad sample quality reported by the device, and a `Mark` field indicating start of anaesthesia.

### ___Hypothesis:___

Data from the two separate source devices can be converted to a common sample rate of 1 Hz and aggregated into a single csv file.

### ___Data:___

[View the visualizations](analysis.php?page=2_images)

### ___Conclusion:___

Case 26 had invalid NIRS data format and was excluded.

CSV files useful for further analysis were produced.

## 3: Data Cleansing <a name="step3"></a>

In this step, anomalies and artefacts in MAP data will be identified by visual inspection of the signal. Any obviously invalid samples will be marked for exclusion.

Invalid values in rSO<sub>2</sub> data have already been marked by the researchers based on field notes and visual inspection. These markings will be incorporated from a separate file. Corrected `Mark` timestamps indicating start of anaesthesia will also be included from this file. The corrections are based on field notes.

A csv file containing the data from step 2, amended with markings described above, will be generated.

### ___Hypothesis:___

There will be artefacts in the blood pressure signal caused by movement and nursing procedures.

### ___Data:___

- Blood pressure data manually marked for exclusion is shaded red.
- Blood pressure data automatically marked as low quality is shaded darker red/grey
- rSO<sub>2</sub> data manually marked for exclusion is shaded purple.
- rSO<sub>2</sub> data automatically marked as low quality is shaded blue.

### Case 00001:

![](images/3_00001_01.png)

### Case 00002:

![](images/3_00002_01.png)

### Case 00003:

![](images/3_00003_01.png)

### Case 00005:

![](images/3_00005_01.png)

### Case 00006:

![](images/3_00006_01.png)

### Case 00007:

![](images/3_00007_01.png)

### Case 00008:

![](images/3_00008_01.png)

### Case 00009:

![](images/3_00009_01.png)

### Case 00010:

![](images/3_00010_01.png)

### ___Conclusion:___

- Any abnormally high or abnormally low MAP readings were marked for exclusion.
- Periodically occurring drops in blood pressure were identified as a NIBP cuff restricting blood flow to the limb used for invasive blood pressure measurement. These values were marked for exclusion.
- The exclusion criteria are pending domain expert review.

A csv file containing the data described above was generated.

## 4: MAP-rSO<sub>2</sub> Scatterplot <a name="step4"></a>

### ___Hypothesis:___

### ___Data:___

### Case 00001:

![](images/4_00001_01.png)
![](images/4_00001_02.png)

### Case 00002:

![](images/4_00002_01.png)
![](images/4_00002_02.png)

### Case 00003:

![](images/4_00003_01.png)
![](images/4_00003_02.png)

### Case 00005:

![](images/4_00005_01.png)
![](images/4_00005_02.png)

### Case 00006:

![](images/4_00006_01.png)
![](images/4_00006_02.png)

### Case 00007:

![](images/4_00007_01.png)
![](images/4_00007_02.png)

### Case 00008:

![](images/4_00008_01.png)
![](images/4_00008_02.png)

### Case 00009:

![](images/4_00009_01.png)
![](images/4_00009_02.png)

### Case 00010:

![](images/4_00010_01.png)
![](images/4_00010_02.png)

### ___Conclusion:___


## 5: Time Synchronization <a name="step5"></a>

It has been noted that the two monitoring devices used for data collection may have a clock discrepancy of several minutes. This is identified as a potential source of error, as the vasogenic phenomena under analysis cycle within 20 to 180 seconds ([_Steiner et al. 2008_](https://doi.org/10.1007/s12028-008-9140-5)).

### ___Hypothesis:___

Automatic synchronization using cross-correlation can be used to reliably align the signals.

__Caveat:__ _Lack of_ correlation between the signals indicates good autoregulation.

### ___Data:___

### Case 00001:

![](images/5_00001_01.png)
![](images/5_00001_02.png)
![](images/5_00001_03.png)
![](images/5_00001_04.png)
![](images/5_00001_05.png)
![](images/5_00001_06.png)
![](images/5_00001_07.png)

### Case 00002:

![](images/5_00002_01.png)
![](images/5_00002_02.png)
![](images/5_00002_03.png)
![](images/5_00002_04.png)
![](images/5_00002_05.png)
![](images/5_00002_06.png)
![](images/5_00002_07.png)

### Case 00003:

![](images/5_00003_01.png)
![](images/5_00003_02.png)
![](images/5_00003_03.png)
![](images/5_00003_04.png)
![](images/5_00003_05.png)
![](images/5_00003_06.png)
![](images/5_00003_07.png)

### Case 00005:

![](images/5_00005_01.png)
![](images/5_00005_02.png)
![](images/5_00005_03.png)
![](images/5_00005_04.png)
![](images/5_00005_05.png)
![](images/5_00005_06.png)
![](images/5_00005_07.png)

### Case 00006:

![](images/5_00006_01.png)
![](images/5_00006_02.png)
![](images/5_00006_03.png)
![](images/5_00006_04.png)
![](images/5_00006_05.png)
![](images/5_00006_06.png)
![](images/5_00006_07.png)

### Case 00007:

![](images/5_00007_01.png)
![](images/5_00007_02.png)
![](images/5_00007_03.png)
![](images/5_00007_04.png)
![](images/5_00007_05.png)
![](images/5_00007_06.png)
![](images/5_00007_07.png)

### Case 00008:

![](images/5_00008_01.png)
![](images/5_00008_02.png)
![](images/5_00008_03.png)
![](images/5_00008_04.png)
![](images/5_00008_05.png)
![](images/5_00008_06.png)
![](images/5_00008_07.png)

### Case 00009:

![](images/5_00009_01.png)
![](images/5_00009_02.png)
![](images/5_00009_03.png)
![](images/5_00009_04.png)
![](images/5_00009_05.png)
![](images/5_00009_06.png)
![](images/5_00009_07.png)

### Case 00010:

![](images/5_00010_01.png)
![](images/5_00010_02.png)
![](images/5_00010_03.png)
![](images/5_00010_04.png)
![](images/5_00010_05.png)
![](images/5_00010_06.png)
![](images/5_00010_07.png)

### ___Conclusion:___

![](scatterplot_quality_small.jpg)

Cross correlation produced sensible results in only part of the cases. Manual alignment was used, based on visual inspection of common patterns between the signals. Part of the cases show no clearly identified point of alignment.

## 6: Scatterplot smoothing <a name="step6"></a>

[___TODO___]: Using a [local regression](https://en.wikipedia.org/wiki/Local_regression) method like the lowess smoother in [Seaborn](https://seaborn.pydata.org/tutorial/regression.html)?

## 7. COx index over time <a name="step7"></a>

[___TODO___]: For BOPRA objective _"To assess the association between time on cerebral blood flow autoregulation range (defined as COx < 0.3) and mortality, morbidity and quality of life."_

This will possibly require patching data discontinuities (imputation) using interpolation or some other method.