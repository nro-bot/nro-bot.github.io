Title: Extracting Cognitive SLUMS Scores from VA Clinical Notes
Starred: false
Date: 2025-01-01 12:00
Category: Computer Science
Slug: VA-SLUMS-NLP
Summary: Rule-based NLP pipeline to extract Saint Louis University Mental Status (SLUMS) scores from ~3 million unstructured VA clinical notes. 83% accuracy, 99% precision, 20,000+ notes/minute on a single laptop. Presented at GSA 2025.
Featured_Image: va_slums.jpg
Website: https://sites.google.com/view/pyslums

*Dr. Nancy Ouyang, Dr. Christine Rizk, Dr. Amir Sharafkhaneh, Sanam Sharafkhaneh, Jose Rios-Monterrosa, Dashiell Helmer, Dr. Javad Razjouyan*
*VA Boston & VA Houston · Presented at GSA 2025*

The **Saint Louis University Mental Status Exam (SLUMS)** is a cognitive screening tool widely used within the US Veterans Healthcare Administration. Scores appear in unstructured clinical notes in dozens of formats — `SLUMS 12/9/15: 24/30`, `16/30 on the SLUMS`, `SLUMS _/30` (blank template) — making automated extraction non-trivial.

We developed a **rule-based NLP pipeline** using regular expressions to extract SLUMS scores from the national VA database, following a five-step development cycle: Conceptualize → Develop → Finalize → Execute → Share.

## Results

- **83% accuracy, 99% precision, 78% F1** on 1,275 hand-annotated notes (two independent annotators + adjudicator)
- Processed **~3 million notes in 2.5 hours** — over 20,000 notes per minute — on a single laptop
- Handles ambiguous cases: blank templates, score-before-SLUMS patterns, exclusion of MOCA/MMSE mentions

## Use Case

Extracted scores enable building tools to screen for mildly (but not severely) impaired patients who may be eligible for clinical trials of new drugs — a population that's hard to identify at scale from structured data alone.

*Funded by the VA.*
