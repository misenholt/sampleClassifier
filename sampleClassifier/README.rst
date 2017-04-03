=========================
Sample Classifier
=========================

 The goal of this project is to build a program that takes unstructured or semi-structured data as input and trains a classifier to classify this data. 
 
 The purpose is to:
 1. Reinforce the skills and knowledge necessary to do so and
 
 2. Add to my portfolio of produced software
 
 
 ========================
 Planning
 ========================
 
 1. Data Aquisition: The data I plan to use is the US Patent Data. This data set is very large and is semi-structured to unstructured. It comes in a variety of formats: xml, sgml, and a proprietary format depending on the year. In addition, fields and variables have changed over the years. 
 
 2. Data Cleaning: I need to establish uniformity of the data I wish to use. This means, for example if I wish to use a heading, there needs to be a heading for every record I wish to use, or at least a consistent proportion of records in every year. The plan is to insert records into a SQL database and then reconcile or remove fields to achieve the desired density. Given the size of the data I may need to use a nosql database.
 
 3. Labelling: Since the data may not come with labels we need to come up with a way to label the data reliably and efficiently (ie not manually). Posibilities include bootstrapping with a seed of pubmed articles, selecting documents that contain terms from a high-confidence list, etc
 
 4. Feature extraction: Select features with consistent enough density to produce results. Text features will need to be tokenized, multigrams identified etc.
 
 5. Train-test: Use classifiers to train and test several types of models over the labelled data. This step may use a randomly selected subset of the entire data set. 
 
 6. Evaluate: Using top-performing models from step 5, classify the entire data set and evaluate the models.

 
 =========================
 AWS Setup
 =========================
 1. launch instance with amazon linux ami
 2. 	sudo yum install python35
		virtualenv -p python35 venv
		source ./venv/bin/activate
 3. copy source code
 4.		export PYTHONPATH=${PYTHONPATH}:${HOME}/sampleClassifier
		mkdir .aws
 5. copy credentials file
 6. 	cd sampleClassifier
		pip install -r requirements.txt
		
		java -jar PatentTransformer.jar --input="2003_pg030107.zip"

		