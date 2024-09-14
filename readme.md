## Требования
Убедитесь, что у вас установлены [Docker](https://www.docker.com/get-started) и [Docker Compose](https://docs.docker.com/compose/install/).

## Запуск проекта
Запустите команду: 
```docker-compose run --rm -e {путь к BED файлу с целевыми последовательностями} -e GENOME_FA={путь к файлу с геномом в формате FASTA} -e INDEXED_GENOME={путь к индексированному геному для выравнивания BWA-MEM} task2 python task2.py```

## Дополнительные параметры
**TARGET_FASTA** - путь к файлу с последовательностями из предоставленного BED файла в формате FASTA.

**OUTPUT_SAM** - путь к файлу с результатами выравнивания BWA-MEM в формате SAM.

**FINAL_OUTPUT** = путь к файлу координатами целевых и найденных нецелевых последовательностей.


## Пример команды запуска
```docker-compose run --rm -e BED_FILE_PATH=IAD143293_241_Designed.bed -e GENOME_FA=hg19.fa -e INDEXED_GENOME=hg19.fa task2 python task2.py ```