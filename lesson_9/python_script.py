import pandas as pd

mass_spec_results = pd.read_csv('/home/input/mass_spec_results.csv')
quality_metrics = pd.read_csv('/home/input/quality_metrics.csv')

# Только образцы, присутствующие в обеих таблицах
inner_join = pd.merge(mass_spec_results, quality_metrics, 
                     on='sample_id', how='inner')
print("Inner Join - только общие образцы:")
print(f"Было: {len(mass_spec_results)} samples -> Стало: {len(inner_join)} samples")
print(inner_join[['sample_id','total_proteins', 'mapping_rate']].head())

# Все образцы из левой таблицы + данные из правой
left_join = pd.merge(mass_spec_results, quality_metrics, 
                    on='sample_id', how='left')
print("Left Join - все образцы из mass_spec_results:")
print(f"Было: {len(mass_spec_results)} samples -> Стало: {len(left_join)} samples")
print("Образцы без quality metrics:")
missing_ms = left_join[left_join['mapping_rate'].isna()]
print(missing_ms[['sample_id', 'total_proteins']])

# Все образцы из правой таблицы + данные из левой
right_join = pd.merge(mass_spec_results, quality_metrics, 
                     on='sample_id', how='right')
print("Right Join - все образцы из quality_metrics:")
print(f"Было: {len(quality_metrics)} samples -> Стало: {len(right_join)} samples")
print("Образцы без mass_spec_results:")
only_in_ms = right_join[right_join['total_proteins'].isna()]
print(only_in_ms[['sample_id', 'mapping_rate']])

# Все образцы из обеих таблиц
outer_join = pd.merge(mass_spec_results, quality_metrics, 
                     on='sample_id', how='outer')
print("Outer Join - все образцы из обеих таблиц:")
print(f"Было: {len(mass_spec_results)} + {len(quality_metrics)} -> Стало: {len(outer_join)}")
print("Статус наличия данных:")
outer_join['has_mass_spec_results'] = ~outer_join['total_proteins'].isna()
outer_join['has_quality_metrics'] = ~outer_join['mapping_rate'].isna()
print(outer_join[['sample_id', 'has_mass_spec_results', 'has_quality_metrics']].value_counts())

# Сохранение в папку output
inner_join.to_csv('/home/output/inner_join.csv', index=False)
left_join.to_csv('/home/output/left_join.csv', index=False)
right_join.to_csv('/home/output/right_join.csv', index=False)
outer_join.to_csv('/home/output/outer_join.csv', index=False)