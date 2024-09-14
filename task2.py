import subprocess
import pandas as pd
import os


class FindHomologousWithBWA:
    def __init__(self, bed_file, genome_fa, indexed_genome, target_fasta='target_sequences.fasta', output_sam='output_alignment.sam', final_output_file='results_with_coordinates.tsv'):
        self.bed_file = bed_file
        self.genome_fa = genome_fa
        self.indexed_genome = indexed_genome
        self.target_fasta = 'target_fasta/' + str(target_fasta)
        self.output_sam = 'output_sam/' + str(output_sam)
        self.final_output_file = 'final_output_file/' + str(final_output_file)

    def get_target_and_nontarget_coordinates(self):
        self.ensure_directories_exist()
        try:
            self.get_fasta_from_bed()
            print(f'Сформирован файл Fasta из файла BED {self.target_fasta}')
        except Exception as e:
            print(e)
        try:
            self.run_bwa()
            print(f'Произведено выравнивание BWA-MEM. Результаты записаны в файл {self.output_sam}')
        except Exception as e:
            print(e)
        try:
            alignment_df = self.parse_sam()
            if not alignment_df.empty:
                alignment_df['100% Homologs'] = alignment_df.apply(self.format_coords, axis=1)
                alignment_df.drop(columns=['chr_align', 'start_align', 'end_align'], inplace=True)
                alignment_df.to_csv(self.final_output_file, index=False, sep='\t', header=True)
                print(f'Файл с координатами целевых и нецелевых регионов сформирован: {self.final_output_file}')
            else:
                print('SAM файл пуст')
        except Exception as e:
            print(e)

    def ensure_directories_exist(self):
        os.makedirs('target_fasta', exist_ok=True)
        os.makedirs('output_sam', exist_ok=True)
        os.makedirs('final_output_file', exist_ok=True)

    def get_fasta_from_bed(self):
        cmd = f"bedtools getfasta -fi {self.genome_fa} -bed {self.bed_file} > {self.target_fasta}"
        subprocess.run(cmd, shell=True, check=True)

    def run_bwa(self):
        cmd = f"bwa mem {self.indexed_genome} {self.target_fasta} > {self.output_sam}"
        subprocess.run(cmd, shell=True, check=True)

    def parse_sam(self):
        results = []
        with (open(self.output_sam, 'r') as f):
            for line in f:
                if line.startswith('@'):
                    continue
                parts = line.split('\t')
                amlocon_name = parts[0]
                chrom_ampl, coords = amlocon_name.split(":")
                start_target, end_target = map(int, coords.split("-"))
                chr_align = parts[2]
                start_align = int(parts[3]) - 1
                len_align = int(parts[5].replace('M', ''))
                end_align = start_align + len_align

                if chrom_ampl != chr_align and not (start_align >= start_target and end_align <= end_target):
                    results.append([amlocon_name, chr_align, start_align, end_align])

        return pd.DataFrame(results, columns=['Amplicon', 'chr_align', 'start_align', 'end_align'])

    @staticmethod
    def format_coords(row):
        return f"{row['chr_align']}:{row['start_align']}-{row['end_align']}"


if __name__ == "__main__":
    prossesor = FindHomologousWithBWA(
        bed_file=os.getenv('BED_FILE_PATH'),
        genome_fa=os.getenv('GENOME_FA'),
        indexed_genome=os.getenv('INDEXED_GENOME'),
        target_fasta=os.getenv('TARGET_FASTA'),
        output_sam=os.getenv('OUTPUT_SAM'),
        final_output_file=os.getenv('FINAL_OUTPUT')
    )
    prossesor.get_target_and_nontarget_coordinates()
