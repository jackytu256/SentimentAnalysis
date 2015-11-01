/**
 * Created by tuhung-te on 1/11/15.
 */

/*          Sentiment_Analysis_individuals       */
// Analysus_Result/sentiment_analysis/All
function(doc) {
		  if(doc.sentiment.senti_Polarity!==0){
                     emit(doc.id,doc.sentiment.senti_Polarity);
		  }

}

// Analysus_Result/sentiment_analysis/AllResults
function(doc) {
		 emit(doc.id,doc)

}

// Analysus_Result/sentiment_analysis/Neg
function(doc) {
  if(doc.sentiment.perception == "neg"){
		  emit(doc.id, doc);
	}
}

// Analysus_Result/sentiment_analysis/NegAndPos
function(doc) {
  if(doc.sentiment.perception == "pos" || doc.sentiment.perception == "neg"){
		  emit(doc.id, doc);
	}
}

// Analysus_Result/sentiment_analysis/Neu
function(doc) {
  if(doc.sentiment.perception == "neu"){
		  emit(doc.id, doc);
	}
}
// Analysus_Result/sentiment_analysis/Pos
function(doc) {
  if(doc.sentiment.perception == "pos"){
		  emit(doc.id, doc);
	}
}




/*          Sentiment_Analysis_Agencies      */
// analysis_result_angecies/sentiment_analysis/All
function(doc) {
		  if(doc.sentiment.senti_Polarity!==0){
                     emit(doc.id,doc.sentiment.senti_Polarity);
		  }

}

// analysis_result_angecies/sentiment_analysis/AllResults
function(doc) {
		 emit(doc.id,doc)

}

// analysis_result_angecies/sentiment_analysis/Neg

function(doc) {
  if(doc.sentiment.perception == "neg"){
		  emit(doc.id, doc);
	}
}

// analysis_result_angecies/sentiment_analysis/NegAndPos
function(doc) {
  if(doc.sentiment.perception == "pos" || doc.sentiment.perception == "neg"){
		  emit(doc.id, doc);
	}
}

//analysis_result_angecies/sentiment_analysis/Neu

function(doc) {
  if(doc.sentiment.perception == "neu"){
		  emit(doc.id, doc);
	}
}

//analysis_result_angecies/sentiment_analysis/Pos
function(doc) {
  if(doc.sentiment.perception == "pos"){
		  emit(doc.id, doc);
	}
}




/*          Elasticsearch_auction      */
//elasticsearch_auction/elastisearch/sentiment_Analysis
function(doc) {
        var regx = [/iauction results/i,/auction result/i,/house price/i,/house prices/i,/property market/i,/property price/i,/property prices/i,/Mortgage/i,/Mortgages/i,/realestate market/i,/auction market/i,/house auctions/i, /doamin auction/i,/expensive property/i,/property bubble/i,/housing bubble/i,/Residential Property/i,/Affordable property/i,/housing market/i,/housing price/i,/bubble risk/i];
	if(doc.text){
		var inRegx = false
		var coordinate = null;
        	for (re in regx){
			if(doc.text.search(regx[re])!=-1){
		        	inRegx = true
				if(doc.coordinates == null){
					coordinate = doc.retweeted_status ? doc.retweeted_status.coordinates:doc.coordinates
				}else{
					coordinate = doc.coordinates
				}

			};
			if(inRegx){
			emit(doc._id, [{"id":doc.id_str,"text":doc.text,"coordinates":coordinate,"time":doc.created_at}])
			break
			}
		}

	}

}

/*          house_price_income_ratio      */
//house_price_income_ratio/bubble/AllResult
function(doc) {
  emit(doc._id,doc);
}


/*          houseingindex_buble      */
//houseingindex_bubble/bubble/AllResult
function(doc) {
  emit(doc._id,doc);
}



/*          housepricewithrenterpayment      */
//housepricewithrenterpayment/bubble/AllResult
function(doc) {
  emit(doc._id,doc);
}

/*          mortgagewithgdp      */
//mortgagewithgdp/bubble/AllResult
function(doc) {
  emit(doc._id,doc);
}


/*          twitter_follow      */
//twitter_follow/sentiment_Analysis/Analysis
function(doc) {
        var regx = [/iauction results/i,/auction result/i,/house price/i,/house prices/i,/property market/i,/property price/i,/property prices/i,/Mortgage/i,/Mortgages/i,/realestate market/i,/auction market/i,/house auctions/i, /doamin auction/i,/expensive property/i,/property bubble/i,/housing bubble/i,/Residential Property/i,/Affordable property/i,/housing market/i,/housing price/i,/auction/i];
	if(doc.info.text){
        	for (re in regx){
		if(doc.info.text.search(regx[re])!=-1){
			emit(doc._id, [{"id":doc._id,"text":doc.info.text,"coordinates":doc.location.coordinates,"time":doc.Time.tweet_posted_timestamp}])
		};
		}
	}

}

/*          twitter_melbourne      */
//twitter_follow/sentiment_analysis/perception_Property
function(doc) {
        var regx = [/iauction results/i,/auction result/i,/house price/i,/house prices/i,/property market/i,/property price/i,/property prices/i,/Mortgage/i,/Mortgages/i,/realestate market/i,/auction market/i,/house auctions/i, /doamin auction/i,/expensive property/i,/property bubble/i,/housing bubble/i,/Residential Property/i,/Affordable property/i,/housing market/i,/housing price/i];
	if(doc.info.text){
        	for (re in regx){
		if(doc.info.text.search(regx[re])!=-1){
				var coordinate = null;
			emit(doc._id, [{"id":doc._id,"text":doc.info.text,"coordinates":doc.location.coordinate,"time":doc.Time.tweet_posted_timestamp}])
		};
		}
	}

}
