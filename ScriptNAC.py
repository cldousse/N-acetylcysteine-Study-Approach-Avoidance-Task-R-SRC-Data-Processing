# “AAT Data Analysis – NAC Study U73 (Traitement data AAT task - NAC Study U73)

# Convert text files into Excel format and store them (Convertir les fichiers txt en fichiers Excel et les enregistrer)
# Exclude trials 1 and 3 (Supprimer les essais 1 et 3)
# Identify corrected and uncorrected errors within each condition (approach, avoidance, and overall) (Identifier les erreurs corrigées et non corrigées dans chaque condition (approche et évitement + total))
# Delete all error trials (Supprimer tous les essais erronés)
# Identify RTs exceeding 5000 ms in the ‘first RTs’ and exclude them (Identifier présence RTs>5000ms dans 'first RTs', si le cas les supprimer)
# Identify and exclude RTs exceeding 3 SDs in the ‘first RTs’ separately for each condition (approach, avoidance) and each stimulus (Neutral vs. Cocaine) (Identifier et éliminer les RTs >3SD dans 'first RTs' pour chaque condition 'approche' et 'évitement' et chaque stim 'Neutre vs. Cocaïne')

import os
import pandas as pd
import csv

##########1. CONVERSION TXT TO EXCEL


# Define folder paths
txt_folder = 'raw_data/'
excel_folder = 'excel_data/'

# Create output folder if it doesn't exist
os.makedirs(excel_folder, exist_ok=True)

# Function to automatically detect the delimiter
def detect_delimiter(file_path, lines_to_read=5):
    with open(file_path, 'r', encoding='latin-1') as f:
        sample = ''.join([f.readline() for _ in range(lines_to_read)])
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
            return dialect.delimiter
        except:
            print(f"[WARNING] Delimiter not detected for {file_path}. Defaulting to comma ','.")
            return ','
# Counters
success_count = 0
failure_count = 0
failed_files = []

# Loop through all .txt files
for filename in os.listdir(txt_folder):
    if filename.lower().endswith('.txt'):
        txt_path = os.path.join(txt_folder, filename)
        base_name = os.path.splitext(filename)[0]
        excel_path = os.path.join(excel_folder, base_name + '.xlsx')

        print(f"\n[INFO] Processing: {filename}")

        delimiter = detect_delimiter(txt_path)
        print(f"[INFO] Detected delimiter: '{delimiter}'")

        try:
            # Try UTF-8, fallback to latin-1
            try:
                df = pd.read_csv(txt_path, delimiter=delimiter, encoding='utf-8')
            except UnicodeDecodeError:
                try: 
                    df = pd.read_csv(txt_path, delimiter=delimiter, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    try: 
                        df = pd.read_csv(txt_path, delimiter=delimiter, encoding='latin-1')
                    except UnicodeDecodeError:
                        try: 
                             df = pd.read_csv(txt_path, delimiter='\t', encoding='utf-16')
                        except: 
                            print ('wrong encoding')


            df.to_excel(excel_path, index=False)
            print(f"[OK] Converted to: {excel_path}")
            success_count += 1

        except Exception as e:
            print(f"[ERROR] Failed to convert {filename}: {e}")
            failure_count += 1
            failed_files.append(filename)

# Final message
print("\n================== SUMMARY ==================")
print(f"✅ {success_count} file(s) successfully converted.")
print(f"❌ {failure_count} file(s) failed to convert.")

if failed_files:
    print("\nFailed files:")
    for file in failed_files:
        print(f" - {file}")
print("=============================================\n")

##########2. REMOVE BLOCKS 1 AND 3 (they are pre-task trial blocks)

# Counters
success_count = 0
failure_count = 0
failed_files = []

# Loop over all Excel files
for filename in os.listdir(excel_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(excel_folder, filename)

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Get the name of the first column
            first_col = df.columns[0]

            # Keep only rows where the first column is 2 or 4
            df_filtered = df[df[first_col].isin([2, 4])]

            # Overwrite the original Excel file
            df_filtered.to_excel(file_path, index=False)
            print(f"[OK] Cleaned and saved: {filename}")
            success_count += 1

        except Exception as e:
            print(f"[ERROR] Could not process {filename}: {e}")
            failure_count += 1
            failed_files.append(filename)

# Final summary
print("\n================== SUMMARY ==================")
print(f"✅ {success_count} file(s) successfully cleaned and saved.")
print(f"❌ {failure_count} file(s) failed to process.")

if failed_files:
    print("\nFailed files:")
    for file in failed_files:
        print(f" - {file}")
print("=============================================\n")

##########3. IDENTIFY CORRECTED vs. UNCORRECTED ERRORS BY CONDITION (toward / away)

# Directory containing the Excel files (Dossier contenant les fichiers Excel)
excel_folder = 'excel_data/'
result_rows = []

# Overall counters (Compteurs globaux)
global_counts = {
    'Toward_corrected': 0,
    'Toward_uncorrected': 0,
    'Away_corrected': 0,
    'Away_uncorrected': 0
}

# Processing the .xlsx files (Parcours des fichiers .xlsx)
for filename in os.listdir(excel_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(excel_folder, filename)
        print(f"\n=== Processing {filename} ===")

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"[ERROR] Could not read {filename}: {e}")
            continue

        # Initialize the counters for this file (Initialisation des compteurs pour ce fichier)
        file_counts = {
            'Toward_corrected': 0,
            'Toward_uncorrected': 0,
            'Away_corrected': 0,
            'Away_uncorrected': 0
        }

        # Iterating row by row (Parcours ligne par ligne)
        for _, row in df.iterrows():
            try:
                A = row.iloc[0]
                D = row.iloc[3]
                F = row.iloc[5]
                J = str(row.iloc[9]).strip().upper()
                M = str(row.iloc[12]).strip().upper()
            except:
                continue  # ignore lines with missing data

            # Toward
            if A == 2:
                if ((D == 1 and F == 1 and J == 'DOWN' and M == 'UP') or
                    (D == 1 and F == 0 and J == 'UP' and M == 'DOWN') or
                    (D == 0 and F == 1 and J == 'UP' and M == 'DOWN') or
                    (D == 0 and F == 0 and J == 'DOWN' and M == 'UP')):
                    file_counts['Toward_corrected'] += 1

                elif ((D == 1 and F == 1 and J == 'DOWN' and M == 'DOWN') or
                    (D == 1 and F == 0 and J == 'UP' and M == 'UP') or
                    (D == 0 and F == 1 and J == 'UP' and M == 'UP') or
                    (D == 0 and F == 0 and J == 'DOWN' and M == 'DOWN')):
                    file_counts['Toward_uncorrected'] += 1

            # Away
            elif A == 4:
                if ((D == 1 and F == 1 and J == 'UP' and M == 'DOWN') or
                    (D == 1 and F == 0 and J == 'DOWN' and M == 'UP') or
                    (D == 0 and F == 1 and J == 'DOWN' and M == 'UP') or
                    (D == 0 and F == 0 and J == 'UP' and M == 'DOWN')):
                    file_counts['Away_corrected'] += 1
                elif ((D == 1 and F == 1 and J == 'UP' and M == 'UP') or
                    (D == 1 and F == 0 and J == 'DOWN' and M == 'DOWN') or
                    (D == 0 and F == 1 and J == 'DOWN' and M == 'DOWN') or
                    (D == 0 and F == 0 and J == 'UP' and M == 'UP')):
                    file_counts['Away_uncorrected'] += 1

         # Compute totals
        total_corrected = file_counts['Toward_corrected'] + file_counts['Away_corrected']
        total_uncorrected = file_counts['Toward_uncorrected'] + file_counts['Away_uncorrected']

          # Store results
        result_rows.append({
            'Filename': filename,
            'Toward_corrected': file_counts['Toward_corrected'],
            'Toward_uncorrected': file_counts['Toward_uncorrected'],
            'Away_corrected': file_counts['Away_corrected'],
            'Away_uncorrected': file_counts['Away_uncorrected'],
            'Total_corrected': total_corrected,
            'Total_uncorrected': total_uncorrected
        })

# Create summary DataFrame
df_results = pd.DataFrame(result_rows)

# Save to CSV
summary_csv_path = os.path.join(excel_folder, 'Summary.csv')
df_results.to_csv(summary_csv_path, index=False)
print("\n✅ DONE — Results saved to:")
print(summary_csv_path)

##########4. RTs are calculated after excluding responses > 500 ms, > 3 SDs, and all erroneous trials (CALCUL DES TRs en éliminant >500ms + >3SD et sans prendre en compte les essais erronés)

from statistics import mean, stdev

result_rows = []

for filename in os.listdir(excel_folder):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(excel_folder, filename)
        print(f"\n=== Processing {filename} ===")

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            print(f"[ERROR] Could not read {filename}: {e}")
            continue

        file_counts = {
            'Toward_corrected': 0,
            'Toward_uncorrected': 0,
            'Away_corrected': 0,
            'Away_uncorrected': 0
        }

        # Preparation of the subgroups (Préparation des sous-groupes)
        values = {
            'T_D1': [],
            'T_D0': [],
            'A_D1': [],
            'A_D0': [],
        }

        for _, row in df.iterrows():
            try:
                A = row.iloc[0]
                D = row.iloc[3]
                F = row.iloc[5]
                I = pd.to_numeric(row.iloc[8], errors='coerce')
                J = str(row.iloc[9]).strip().upper()
                M = str(row.iloc[12]).strip().upper()
            except:
                continue

            if pd.isnull(I) or I > 5000:
                continue  # Remove missing or outlier values (exclure les valeurs manquantes ou extrêmes)

            is_error = False

            if A == 2:
                if ((D == 1 and F == 1 and J == 'DOWN' and M == 'UP') or
                    (D == 1 and F == 0 and J == 'UP' and M == 'DOWN') or
                    (D == 0 and F == 1 and J == 'UP' and M == 'DOWN') or
                    (D == 0 and F == 0 and J == 'DOWN' and M == 'UP')):
                    file_counts['Toward_corrected'] += 1
                    is_error = True
                elif ((D == 1 and F == 1 and J == 'DOWN' and M == 'DOWN') or
                      (D == 1 and F == 0 and J == 'UP' and M == 'UP') or
                      (D == 0 and F == 1 and J == 'UP' and M == 'UP') or
                      (D == 0 and F == 0 and J == 'DOWN' and M == 'DOWN')):
                    file_counts['Toward_uncorrected'] += 1
                    is_error = True

            elif A == 4:
                if ((D == 1 and F == 1 and J == 'UP' and M == 'DOWN') or
                    (D == 1 and F == 0 and J == 'DOWN' and M == 'UP') or
                    (D == 0 and F == 1 and J == 'DOWN' and M == 'UP') or
                    (D == 0 and F == 0 and J == 'UP' and M == 'DOWN')):
                    file_counts['Away_corrected'] += 1
                    is_error = True
                elif ((D == 1 and F == 1 and J == 'UP' and M == 'UP') or
                      (D == 1 and F == 0 and J == 'DOWN' and M == 'DOWN') or
                      (D == 0 and F == 1 and J == 'DOWN' and M == 'DOWN') or
                      (D == 0 and F == 0 and J == 'UP' and M == 'UP')):
                    file_counts['Away_uncorrected'] += 1
                    is_error = True

            # Retain only error-free rows (Stocker uniquement les lignes sans erreur)
            if not is_error:
                if A == 2 and D == 1:
                    values['T_D1'].append(I)
                elif A == 2 and D == 0:
                    values['T_D0'].append(I)
                elif A == 4 and D == 1:
                    values['A_D1'].append(I)
                elif A == 4 and D == 0:
                    values['A_D0'].append(I)

        # Data cleaning + stats calculation function (Fonction de nettoyage + calcul stats)
        def compute_stats(val_list):
            if len(val_list) < 3:
                return (len(val_list), None, None, 0)
            m = mean(val_list)
            s = stdev(val_list)
            filtered = [v for v in val_list if abs(v - m) <= 3 * s]
            outliers = len(val_list) - len(filtered)
            return (len(filtered), round(mean(filtered), 2), round(stdev(filtered), 2) if len(filtered) > 1 else None, outliers)

        T_D1_n, T_D1_mean, T_D1_std, T_D1_out = compute_stats(values['T_D1'])
        T_D0_n, T_D0_mean, T_D0_std, T_D0_out = compute_stats(values['T_D0'])
        A_D1_n, A_D1_mean, A_D1_std, A_D1_out = compute_stats(values['A_D1'])
        A_D0_n, A_D0_mean, A_D0_std, A_D0_out = compute_stats(values['A_D0'])

        total_corrected = file_counts['Toward_corrected'] + file_counts['Away_corrected']
        total_uncorrected = file_counts['Toward_uncorrected'] + file_counts['Away_uncorrected']

        result_rows.append({
            'Filename': filename,
            'Toward_corrected': file_counts['Toward_corrected'],
            'Toward_uncorrected': file_counts['Toward_uncorrected'],
            'Away_corrected': file_counts['Away_corrected'],
            'Away_uncorrected': file_counts['Away_uncorrected'],
            'Total_corrected': total_corrected,
            'Total_uncorrected': total_uncorrected,
            'TowardCocaïne_ImageNeutral_mean': T_D1_mean,
            'TowardCocaïne_ImageNeutral_std': T_D1_std,
            'TowardCocaïne_ImageNeutral_outliers': T_D1_out,
            'TowardCocaïne_ImageCocaïne_mean': T_D0_mean,
            'TowardCocaïne_ImageCocaïne_std': T_D0_std,
            'TowardCocaïne_ImageCocaïne_outliers': T_D0_out,
            'AwayCocaïne_ImageNeutral_mean': A_D1_mean,
            'AwayCocaïne_ImageNeutral_std': A_D1_std,
            'AwayCocaïne_ImageNeutral_outliers': A_D1_out,
            'AwayCocaïne_ImageCocaïne_mean': A_D0_mean,
            'AwayCocaïne_ImageCocaïne_std': A_D0_std,
            'AwayCocaïne_ImageCocaïne_outliers': A_D0_out,
        })

# Export
df_results = pd.DataFrame(result_rows)
summary_csv_path = os.path.join(excel_folder, 'Summary.csv')
df_results.to_csv(summary_csv_path, index=False)
print(f"\n✅ DONE — Final summary saved to:\n{summary_csv_path}")

##########5. CALCULATION OF SRC SCORES

# Load the CSV file (Charger le CSV)
summary_csv_path = 'excel_data/Summary.csv'
df = pd.read_csv(summary_csv_path)

# Compute SRC scores (Calcul des scores SRC)
df['SRCscore_ImageNeutral'] = df['AwayCocaïne_ImageNeutral_mean'] - df['TowardCocaïne_ImageNeutral_mean']
df['SRCscore_ImageCocaïne'] = df['AwayCocaïne_ImageCocaïne_mean'] - df['TowardCocaïne_ImageCocaïne_mean']

# Save the updated dataset (Sauvegarder le tableau mis à jour)
# Extract the leading number from the filename for sorting (Extraire un nombre au début du nom du fichier pour trier)
df['SortKey'] = df['Filename'].str.extract(r'(\d+)').astype(float)

# Sort based on this numeric key (Trier selon cette clé numérique)
df = df.sort_values(by='SortKey').drop(columns='SortKey')

df.to_csv(summary_csv_path, index=False)

print(f"\n✅ SRC scores calculated and saved to:\n{summary_csv_path}")
