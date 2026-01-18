# Medical Retrieval System

This project implements a RAG system for medical abstracts using `ElasticSearch`, `LangGraph`, `Gemini` and `FastAPI`

The system helps retrieve and summarize information from historical medical abstracts such as:
- Similar reported cases
- Treatments or interventions used
- outcomes or complications observed


### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environmental variables
```bash
# rename `example.env` to `.env`
# update your API key respectively
```

### Run Application
```bash
uvicorn app:app --reload
```

### Example Executions
```bash
# search request
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
        "query": "Has Bell’s palsy been reported and how was it managed?"
      }'

# response
{"status":"success","results":[{"id":"B0YczZsBtKlyZfIK6bQf","_score":0.9072539,"condition":"nervous system diseases","record":"Limited selective posterior rhizotomy for the treatment of spasticity secondary to infantile cerebral palsy: a preliminary report. A limited selective posterior rhizotomy was performed on 30 children suffering from spasticity secondary to infantile cerebral palsy. As opposed to standard techniques that stimulate and divide the dorsal rootlets from L2 to S1, we dissected L4, L5, and S1 dorsal roots through an L5 to S1 laminectomy. Eight to 12 rootlets from each root were electrically stimulated with two unipolar electrodes (pulse width, 50 microseconds; 10-50 V). The muscle responses were observed visually and registered by electromyography. Those rootlets associated with an abnormal motor response as evidenced by sustained muscular contraction or by prolonged electromyographic response were divided. Spasticity was scored from 0 to +. The muscular groups assessed were those involved in the flexion of the shoulder, elbow and wrist in the upper limbs, and those involved in flexion and adduction of the hip, flexion of the leg, and plantar flexion in the lower limbs. The patients were assessed 1 week before and 6 months after the operation. Reduction of spasticity was observed in all the muscular groups, and all the patients presented functional improvement of motor abilities. These preliminary results indicate that a limited procedure that reduces the extension of the laminectomy and the length of the operation could be effective for treating spasticity secondary to infantile cerebral palsy. "},{"id":"ukYnzZsBtKlyZfIKfLWh","_score":0.9062542,"condition":"nervous system diseases","record":"Posterior transfer of the adductors in children who have cerebral palsy. A long-term study. Seventy-eight posterior transfers of the adductors of the hip in forty-two children who has spastic cerebral palsy were reviewed an average of 5.7 years after the operation (range, two to 14.6 years). The results were assessed on the basis of the patient's ability to walk, the range of motion of the affected hip or hips, and the radiographic measurements. In 88 per cent of the patients, the transfer was successful in improving or maintaining abduction, extension, functional walking, and stability of the hip. The failures were all in patients who were unable to walk and who had spastic quadriplegia. Tenotomy of the iliopsoas tendon at the time of the transfer procedure resulted in an improved range of motion of the hip. "},{"id":"IkYczZsBtKlyZfIK-rRv","_score":0.90314406,"condition":"nervous system diseases","record":"Sternocleidomastoid muscle transfer and superficial musculoaponeurotic system plication in the prevention of Frey's syndrome Parotidectomy may be associated with a significant depression in the retromandibular region and a significant incidence of gustatory sweating (Frey's syndrome). Superiorly and inferiorly based sternocleidomastoid flaps and posterior plication of the superficial musculoaponeurotic system were evaluated for their ability to ameliorate both consequences. Sixteen patients with sternocleidomastoid flaps and 16 patients with superficial musculoaponeurotic system plication were compared to a control group of 104 patients. The incidence of Frey's syndrome was 47.1% in the control group, 12.5% (P = 0.025) in the sternocleidomastoid flap group, and 0% (P = 0.005) in the superficial musculoaponeurotic system plication group. The surgical techniques are described. The prevalence of Frey's syndrome is discussed with respect to age, sex, radiation therapy, and the type of parotidectomy performed. The indications and contraindications of the three surgical techniques are described. "},{"id":"y0YnzZsBtKlyZfIKH7Q9","_score":0.90203995,"condition":"nervous system diseases","record":"The floppy infant: recent advances in the understanding of disorders affecting the neuromuscular junction. The clinician is often asked to evaluate the floppy infant. Numerous conditions that cause hypotonia in infancy are briefly outlined in this article. These conditions may affect the brain, spinal cord, or motor unit. Several disorders of neuromuscular transmission, including four distinct and recently described congenital myasthenic syndromes and infant botulism, are discussed thereafter. "},{"id":"NkYdzZsBtKlyZfIKCrRV","_score":0.90155756,"condition":"nervous system diseases","record":"Congenital myasthenia associated with facial malformations in Iraqi and Iranian Jews. A new genetic syndrome. Fourteen Jewish patients from 10 families of either Iraqi or Iranian origin with congenital myasthenia had associated facial malformations which included an elongated face, mandibular prognathism with class III malocclusion and a high-arched palate. Other common features were muscle weakness restricted predominantly to ptosis, weakness of facial and masticatory muscles, and fatigable speech; mild and nonprogressive course; response to cholinesterase inhibitors; absence of antibodies to acetylcholine receptor; decremental response on repetitive stimulation at 3 Hz but no repetitive compound muscle action potential in response to a single nerve stimulus. This newly recognized form of congenital myasthenia with distinctive ethnic clustering and associated facial malformations is transmitted as an autosomal recessive disorder. The facial abnormalities may be secondary to the neuromuscular defect or may be primary and unrelated. Further studies are needed to elucidate the defect in neuromuscular transmission responsible for the pathogenesis of this syndrome. "}]}

```
**QA request**
```bash
curl -X POST "http://localhost:8000/qa" \
  -H "Content-Type: application/json" \
  -d '{
        "question": "Has Bell’s palsy been reported and how was it managed?"
      }'

# response
{"status":"success","message":"Yes, the context mentions \"Mohs micrographic surgery fixed-tissue technique for melanoma of the nose.\" It states that this technique offers benefits such as ensuring eradication of the main tumor mass and its silent outgrowths, managing non-contiguous satellites, and sparing maximal amounts of surrounding normal tissue."}
```