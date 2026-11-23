# Load discovery helpers without re-running its initial search jobs.
exec(open('batches/glossary_batch_product_manager/working/discover_videos.py').read().split('jobs=[]')[0])
queries={'customer_interviews':'user research interviews tutorial','jobs_to_be_done_framework':'jobs to be done explained','impact_assessment':'product prioritization impact assessment','cross_functional_collaboration':'cross functional team collaboration','launch_communication_plan':'product launch communication plan','product_requirements_document':'how to write PRD product requirements document','product_market_fit':'product market fit explained retention','feature_sequencing':'feature sequencing product roadmap dependencies','quarterly_planning':'quarterly planning product management'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for key,rows,err in pool.map(lambda a:fetch(*a),queries.items()):print(key,len(rows),err)
