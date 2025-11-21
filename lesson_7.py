#!/usr/bin/env python
# coding: utf-8

# In[107]:


import requests
import pandas as pd
import xml.etree.ElementTree as ET
import json


# Задание 1

# In[16]:


# Формируем URL (используем параметры)
base_url = "https://www.ebi.ac.uk/proteins/api/features"
params = {'accession': 'P04637'}  # Параметры запроса

# Отправляем GET-запрос
response = requests.get(base_url, params=params)

# Проверяем успешность запроса
if response.status_code == 200:
    data = response.json()  # Парсим JSON-ответ
    print(data[0]['features'])
else:
    print(f"Ошибка! Код: {response.status_code}")


# Задание 2

# In[31]:


base_url = f"https://www.ebi.ac.uk/proteins/api/features" 
params = {
    'accession': 'P05067,P10636'  # через запятую в одном параметре
}# Параметры запроса

# Отправляем GET-запрос
response = requests.get(base_url, headers={"Accept": "application/json"}, params=params)

# Проверяем успешность запроса
if response.status_code == 200:
    data = response.json()  # Парсим JSON-ответ
    for i in range(2):
        print('Белок:', data[i]['accession'])
        print('Последовательность:', data[i]['sequence'], f"длиной {len(data[i]['sequence'])} аминокислот")
else:
    print(f"Ошибка! Код: {response.status_code}")


# Задание 3

# In[47]:


requestURL = "https://www.ebi.ac.uk/proteins/api/proteins" 
params = {
    'offset':0,
    'size':100,
    'taxid': '9606'
}

ids = []

r = requests.get(requestURL, headers={ "Accept" : "application/json"}, params=params)

if r.status_code == 200:
    data = r.json()# Парсим JSON-ответ
    for i in range(5):
        ids.append(data[i]['accession'])
        print(data[i]['accession'])
else:
    print(f"Ошибка! Код: {r.status_code}")


# In[50]:


base_url = f"https://www.ebi.ac.uk/proteins/api/features" 
params = {'offset':0,
    'size':100,
    'accession': ','.join(ids)  # через запятую в одном параметре
}

d = {'accession': [], 'entryName': [], 'seq_length': []} 
response = requests.get(base_url, headers={"Accept": "application/json"}, params=params)

# Проверяем успешность запроса
if response.status_code == 200:
    data = response.json()  # Парсим JSON-ответ
    for i in range(5):
        d['accession'].append(data[i]['accession'])
        d['entryName'].append(data[i]['entryName'])
        d['seq_length'].append(len(data[i]['sequence']))
else:
    print(f"Ошибка! Код: {response.status_code}")


# In[53]:


df = pd.DataFrame(d)
df


# Задание 4

# In[61]:


base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    'db': 'pubmed',
    'term': 'COVID-19 variants',
    'retmode': 'json',
    'sort': 'pub_date',
    'retmax': 10  # Ограничиваем результат 5 статьями
}

response = requests.get(base_url, params=params)
data = response.json()

id_list = data['esearchresult']['idlist']
print("Найденные ID статей:", id_list)


# In[67]:


fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
fetch_params = {
        'db': 'pubmed',
        'id': ','.join(id_list),
        'retmode': 'json'
    }
fetch_response = requests.get(fetch_url, params=fetch_params)
data = fetch_response.json()  
for i, article_id in enumerate(id_list, 1):
    article_data = data.get('result', {}).get(article_id, {})
    title = article_data.get('title', 'Заголовок не найден')
    date = article_data.get('pubdate', 'Дата не указана')
    print(f"{i}. ID: {article_id}")
    print(f"   Дата: {date}")
    print(f"   Заголовок: {title}")
    print("-" * 80)


# Задание 5

# In[71]:


def get_protein_name(accession):
    base_url = "https://www.ebi.ac.uk/proteins/api/features"
    params = {'accession': accession}  # Параметры запроса
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()  # Парсим JSON-ответ
        return data[0]['entryName']
    elif response.status_code == 404:
        print(f"Ошибка! белок не найден")
    else:
        print('белок не найлен, исправьте запрос')


# In[72]:


get_protein_name('fhhjjm')


# Задание 6

# In[78]:


try:
    with open('accessions.txt', 'r', encoding='utf-8') as f:
        accessions = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Файл {'accessions.txt'} не найден!")

url = f"https://www.ebi.ac.uk/proteins/api/proteins"
params = {'accession': ','.join(accessions)}
response = requests.get(
            url,
            headers={'Accept': 'application/json'},
            params=params
        )
        
if response.status_code == 200:
    data = response.json()
    with open('output.txt', 'w', encoding='utf-8') as f:
        for i in range(len(data)):
            protein_name = data[i].get('protein', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Не найдено')
            organism = data[i].get('organism', {}).get('name', {}).get('value', 'Не найдено')
            f.write(f"{data[i]['accession']}\t{protein_name}\t{organism}\n")
            
else:
    print(f"Ошибка! Код: {response.status_code}")


# Задание 7

# In[85]:


fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
fetch_params = {
        'db': 'pubmed',
        'id': ','.join(id_list),
        'retmode': 'xml'
    }
fetch_response = requests.get(fetch_url, params=fetch_params)

if fetch_response.status_code == 200:
    root = ET.fromstring(fetch_response.content)
    for article in root.findall('.//PubmedArticle'):
        title = article.find('.//ArticleTitle')
        title_text = title.text if title is not None else 'N/A'
        
        authors = []
        author_list = article.find('.//AuthorList')
    
        if author_list is not None:
            for author in author_list.findall('Author'):
                last_name = author.find('LastName')
                fore_name = author.find('ForeName')
                collective_name = author.find('CollectiveName')
                
                if collective_name is not None and collective_name.text:
                    authors.append(collective_name.text)
                elif last_name is not None and last_name.text:
                    full_name = f"{last_name.text}"
                    if fore_name is not None and fore_name.text:
                        full_name += f" {fore_name.text}"
                    authors.append(full_name)
        print(f"{title_text} авторы {authors}")
else:
    print(f"Ошибка! Код: {fetch_response.status_code}")


# Задание 8

# ```
# curl -s "https://www.ebi.ac.uk/proteins/api/proteins/P05067" | grep -i "phosphorylation" | head -1
# ```

# Задание 9

# ```
# curl -s "https://www.ebi.ac.uk/proteins/api/features/Q8WZ42" | jq -r '.sequence' | fold -w 80 | head -5
# ```
# 
# Вывод 
# >MTTQAPTFTQPLQSVVVLEGSTATFEAHISGFPVPEVSWFRDGQVISTSTLPGVQISFSDGRAKLTIPAVTKANSGRYSL
# >KATNGSGQATSTAELLVKAETAPPNFVQRLQSMTVRQGSQVRLQVRVTGIPTPVVKFYRDGAEIQSSLDFQISQEGDLYS
# >LLIAEAYPEDSGTYSVNATNSVGRATSTAELLVQGEEEVPAKKTKTIVSTAQISESRQTRIEKKIEAHFDARSIATVEMV
# >IDGAAGQQLPHKTPPRIPPKPKSRSPTPPSIAAKAQLARQQSPSPIRHSPSPVRHVRAPTPSPVRSVSPAARISTSPIRS
# >VRSPLLMRKTQASTVATGPEVPPPWKQEGYVASSSEAEMRETTLTTSTQIRTEERWEGRYGVQEQVTISGAAGAAASVSA

# Задание 10

# Подсчет количества аннотации типа VARIANT
# ```
# curl -s "https://www.ebi.ac.uk/proteins/api/features/P00533" | jq '[.features[] | select(.type == "VARIANT")] | length'
# ```
# Ответ: 40
# 
# ```
# curl -s "https://www.ebi.ac.uk/proteins/api/features/P00533" | jq '.features[] | select(.type == "VARIANT") | {begin, end, description, alternativeSequence}' | head -10
# ```
# Вывод
# ```
# {
#   "begin": "30",
#   "end": "297",
#   "description": "variant EGFR vIII; found in a lung cancer sample; somatic mutation; induces lung cancer when exogenously expressed",
#   "alternativeSequence": ""
# }
# {
#   "begin": "98",
#   "end": "98",
#   "description": "in dbSNP:rs17289589",
# ```

# Задание 12

# In[89]:


gene_name = 'APOE'
url = "https://rest.uniprot.org/uniprotkb/search"
params = {
        'query': f'gene:{gene_name} AND organism_id:9606',
        'format': 'json',
        'size': 100,
        'fields': 'accession'
    }
response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
        
data = response.json()
accessions = []
        
for result in data.get('results', []):
    accession = result.get('primaryAccession', 'N/A')
    uniprot_link = f"https://www.uniprot.org/uniprot/{accession}"
    accessions.append(uniprot_link)


# In[90]:


accessions


# Задание 13

# In[93]:


def optimized_request(accessions):
    # accessions - параметр где должен быть список accession id для искомых белков
    url = f"https://www.ebi.ac.uk/proteins/api/proteins" 
    params = {'offset':0,
              'size':100,
              'accession': ','.join(accessions)  # через запятую в одном параметре
             }
    response = requests.get(url, headers={"Accept": "application/json"}, params=params)
    if response.status_code == 200:
        data = response.json()  # Парсим JSON-ответ
        return data # в виде списка
    else:
        print(f"Ошибка! Код: {response.status_code}")


# In[94]:


optimized_request(['P04637', 'P05067', 'P10636'])


# Задание 16

# In[101]:


base_url = "https://www.ebi.ac.uk/proteins/api/proteins"

params = {
    'taxid': '9606',
    'keyword': 'transcription factor',
    'size': 100,
    'offset': 0
}

try:
    response = requests.get(base_url, params=params, headers={'Accept': 'application/json'})
    data = response.json()
    print(len(data))
except Exception as e:
    print(f"Ошибка: {e}")


# Задание 18

# In[103]:


def simple_gene_to_pubmed(gene_name):
    # Поиск белка в EBI Proteins API
    proteins_url = "https://www.ebi.ac.uk/proteins/api/proteins"
    proteins_params = {
        'gene': gene_name,
        'taxid': '9606',
        'size': 1
    }
    
    try:
        proteins_response = requests.get(proteins_url, params=proteins_params, headers={'Accept': 'application/json'})
        
        if proteins_response.status_code == 200:
            proteins_data = proteins_response.json()
            accession = proteins_data[0].get('accession', 'N/A')
        else:
            print(f"Ошибка Proteins API: {proteins_response.status_code}")
            return []
            
    except Exception as e:
        print(f" Ошибка: {e}")
        return []
    
    # Поиск статей в PubMed
    pubmed_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    pubmed_params = {
        'db': 'pubmed',
        'term': f'{gene_name}[Gene Name] AND human[Organism]',
        'retmode': 'json',
        'retmax': 50,
        'sort': 'relevance'
    }
    
    try:
        pubmed_response = requests.get(pubmed_url, params=pubmed_params)
        
        if pubmed_response.status_code == 200:
            pubmed_data = pubmed_response.json()
            article_ids = pubmed_data.get('esearchresult', {}).get('idlist', [])
            for i, article_id in enumerate(article_ids, 1):
                print(f"{i}. {article_id}")
            return article_ids   
        else:
            print(f" Ошибка PubMed API: {pubmed_response.status_code}")
            return []
            
    except Exception as e:
        print(f" Ошибка: {e}")
        return []


# In[104]:


simple_gene_to_pubmed('EGFR')


# Задание 19

# In[108]:


url = "https://www.ebi.ac.uk/proteins/api/proteins/P04637"

headers = {
    'Accept': 'application/json'
}
response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

# Сохраняем в JSON файл
with open('protein_accession.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)


# Команда которая требовалась в задании:
# ```
# jq -r '.accession // .[0].accession // empty' protein_accession.json 2>/dev/null
# ```
# Вывод: P04637, все совпадает 
