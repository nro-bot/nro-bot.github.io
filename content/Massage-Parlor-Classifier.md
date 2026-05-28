Title: PhD Thesis: NLP for Uncovering the Illicit Massage Industry
Starred: true
Date: 2023-09-05 12:00
Category: Computer Science
Slug: Massage-Parlor-Classifier
Summary: PhD thesis (Harvard, Sep 2023) applying NLP and finetuned BERT models to classify online massage parlor reviews, enabling geographic analysis of illicit activity to support counter-trafficking research.
Featured_Image: thesis_thumb.jpg
Video: https://www.youtube.com/watch?v=Om8fdqSQyJ8
Slides: https://docs.google.com/presentation/d/1NfrZYWBR5R8XLGmo2f1VieHoT9Ir4HzBtAmoWcDCrJU/edit
Arxiv: https://arxiv.org/abs/2309.03470

*PhD Thesis Defense — Harvard SEAS, September 2023*

How can computer science be used to fight human trafficking? I use natural language processing (NLP) to monitor the United States illicit massage industry (IMI), a multi-billion dollar industry that offers not just therapeutic massages but also commercial sexual services. Employees of this industry are often immigrant women with few job opportunities, leaving them vulnerable to fraud, coercion, and other facets of human trafficking. Monitoring spatiotemporal trends helps prevent trafficking in the IMI. By creating datasets with three publicly-accessible websites: Google Places, Rubmaps, and AMPReviews, combined with NLP techniques such as bag-of-words and Word2Vec, I show how to derive insights into the labor pressures and language barriers that employees face, as well as the income, demographics, and societal pressures affecting sex buyers. I include a call-to-action to other researchers given these datasets.

A subset of massage parlors have illicit activity alongside legitimate services. These locations accrue reviews on both mainstream platforms (Google Maps) and niche platforms (Rubmaps). By training a classifier to extrapolate from the more-labeled niche dataset to the mainstream dataset, researchers can estimate the geographic distribution and intensity of illicit activity — supporting counter-trafficking investigation and policy.

![Heatmap of online illicit massage parlor review activity during COVID-19, by month](/Massage-Parlor-Classifier/massage_classifier.jpg)
*Review-volume analysis across 2020 — illicit-activity review patterns shifted noticeably during COVID-19 shutdowns.*

**What I did:** Solo work using Python and the [SimpleTransformers](https://simpletransformers.ai/) library to finetune BERT models on this NLP binary classification task. Standard data science stack (pandas, numpy, matplotlib, seaborn, scipy, sklearn) for exploratory analysis, including review-volume time series across 2020. Data from Heyrick Research courtesy of IBM.

![](/Massage-Parlor-Classifier/posts_per_day.png)

![](/Massage-Parlor-Classifier/screenshot_places.png)

![](/Massage-Parlor-Classifier/BARPLOT_covariates.png)

![](/Massage-Parlor-Classifier/result_logreg.png)

PhD advisor: Prof. Roberto Rigobon. Prior collaborations with Prof. Robert Platt (Northeastern) and Prof. Robert Howe (Harvard).
