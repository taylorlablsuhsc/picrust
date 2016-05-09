# picrust
Piscrust SOP
######################################
mkdir $PWD/secondary_analysis/picrust
#deactivate qiime;rerep seqs first
xton_remover.py -i $PWD/filtered.fna -o $PWD/secondary_analysis/picrust/singleton_filtered.fna
#remove chimeras
#greengenes database not recommended to remove chimeras, use rdp_gold.fa
#activate qiime18, qiime19 passes unexpected "thread" argument into identify_chimeric_seqs.py
echo "removing chimeras from singleton_filtered.fna, fast"
#vsearch for large files (64 bit)
vsearch --uchime_ref $PWD/secondary_analysis/picrust/singleton_filtered.fna --db /media/nfs_opt/bin/gold.fa --nonchimeras $PWD/secondary_analysis/picrust/seqs_chimeras_singleton_filtered.fna
echo "pick_otus:enable_rev_strand_match False"  >> $PWD/secondary_analysis/picrust/otu_picking_params_97.txt
echo "pick_otus:similarity 0.97" >> $PWD/secondary_analysis/picrust/otu_picking_params_97.txt
#note: closed_reference tree file is located in greengenes folder; use "unannotated" copy
pick_closed_reference_otus.py -i $PWD/secondary_analysis/picrust/seqs_chimeras_singleton_filtered.fna -o $PWD/secondary_analysis/picrust/ -p $PWD/secondary_analysis/picrust/otu_picking_params_97.txt -r /home/vince/code/PICRUSt/picrust_download/picrust/picrust/data/gg_13_8_otus/rep_set/97_otus.fasta -t /home/vince/code/PICRUSt/picrust_download/picrust/picrust/data/gg_13_8_otus/taxonomy/97_otu_taxonomy.txt -f -a -0 40
#convert for inspection
biom convert -i $PWD/secondary_analysis/picrust/otu_table.biom -o $PWD/secondary_analysis/picrust/otu_table_json.biom --to-json
sed -i 's/None/k__None/g' $PWD/secondary_analysis/picrust/otu_table_json.biom
sed -i 's/Unclassified/k__None/g' $PWD/secondary_analysis/picrust/otu_table_json.biom
# deactivate qiime, activate PICRUSt, if h5py is present, bioms will be HDF5
cd $PWD/secondary_analysis/picrust/ucrC97/
normalize_by_copy_number.py -i otu_table.biom -o normalized_closed_hdf5.biom
predict_metagenomes.py -i normalized_closed_hdf5.biom -o metagenome_normalized_closed_hdf5.biom
biom convert -i metagenome_normalized_closed_hdf5.biom -o table_metagenome.txt --to-tsv --header-key KEGG_Pathways
categorize_by_function.py -i metagenome_normalized_closed_hdf5.biom -o cat_by_func_metagenome_L3.biom -c KEGG_Pathways -l 3
