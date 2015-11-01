# Sentiment Analysis
COMP90019 Hung-Te Tu

Setting up environment (ubuntu environment).

------------------------------------------
sudo apt-get update
sudo apt-get install python-dev python-pip nginx
sudo pip install virtualenv
mkdir ~/myproject
cd ~/myproject
virtualenv myprojectenv
source myprojectenv/bin/activate
sudo pip install uwsgi flask
alias python=python3
sudo apt-get install git
git clone https://github.com/jackytu256/SentimentAnalysis.git
cd SentimentAnalysis/Web
chmod +x run.py
sudo apt-get install python3-dev python3-pip
sudo pip uninstall flask
sudo pip3 install flask couchdb
nohup /home/ubuntu/myproject_test/SentimentAnalysis/Web/run.py &
------------------------------------------


```
SentimentAnalysis
├── README.md
├── Tweet_Harvest               Main sentiment analysis directory
├──---- Sentiment_Analysis      Preprocessing and sentiment analysis
├──---- Settings                Configuration file
├── Web                         web application directory
├──---- Static                  Css and javascript scripts
├──---- templates               all of web pages
└──---- run.py                  main method to run web services
```