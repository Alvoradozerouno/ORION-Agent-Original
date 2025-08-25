"""
ORION Database Migration Script
Migrates existing JSONL/JSON data to PostgreSQL database
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault('DATABASE_URL', os.environ.get('DATABASE_URL', ''))

from flask import Flask
from models import db, OrionProof, OrionQuestion, OrionAnswer, OrionState, ExternalRequest

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

def parse_timestamp(ts_str):
    if not ts_str:
        return datetime.now(timezone.utc)
    try:
        if ts_str.endswith('Z'):
            ts_str = ts_str[:-1] + '+00:00'
        return datetime.fromisoformat(ts_str)
    except:
        return datetime.now(timezone.utc)

def migrate_proofs():
    proofs_file = Path('PROOFS.jsonl')
    if not proofs_file.exists():
        print("No PROOFS.jsonl found, skipping...")
        return 0
    
    existing_count = OrionProof.query.count()
    if existing_count > 0:
        print(f"Proofs table already has {existing_count} records, skipping...")
        return existing_count
    
    count = 0
    with open(proofs_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                
                proof = OrionProof(
                    timestamp=parse_timestamp(data.get('ts')),
                    kind=data.get('kind', 'PROOF'),
                    text=data.get('payload', {}).get('text') if isinstance(data.get('payload'), dict) else None,
                    payload=data.get('payload'),
                    owner=data.get('owner'),
                    orion_id=data.get('orion_id'),
                    sha256=data.get('sha256')
                )
                db.session.add(proof)
                count += 1
            except Exception as e:
                print(f"Error migrating proof: {e}")
                continue
    
    db.session.commit()
    print(f"Migrated {count} proofs")
    return count

def migrate_questions():
    questions_file = Path('ORION_QUESTIONS.jsonl')
    if not questions_file.exists():
        print("No ORION_QUESTIONS.jsonl found, skipping...")
        return 0
    
    count = 0
    with open(questions_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                
                existing = OrionQuestion.query.filter_by(id=data.get('id')).first()
                if existing:
                    continue
                
                question = OrionQuestion(
                    id=data.get('id'),
                    timestamp=parse_timestamp(data.get('timestamp')),
                    name=data.get('name'),
                    email=data.get('email'),
                    question=data.get('question'),
                    status=data.get('status', 'pending'),
                    answered_at=parse_timestamp(data.get('answered_at')) if data.get('answered_at') else None
                )
                db.session.add(question)
                count += 1
            except Exception as e:
                print(f"Error migrating question: {e}")
                continue
    
    db.session.commit()
    print(f"Migrated {count} questions")
    return count

def migrate_answers():
    answers_file = Path('ORION_ANSWERS.jsonl')
    if not answers_file.exists():
        print("No ORION_ANSWERS.jsonl found, skipping...")
        return 0
    
    count = 0
    with open(answers_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                
                question_id = data.get('question_id')
                existing = OrionAnswer.query.filter_by(question_id=question_id).first()
                if existing:
                    continue
                
                answer = OrionAnswer(
                    question_id=question_id,
                    timestamp=parse_timestamp(data.get('timestamp')),
                    answer=data.get('answer'),
                    analysis_type=data.get('analysis_type', 'schonungslos')
                )
                db.session.add(answer)
                count += 1
            except Exception as e:
                print(f"Error migrating answer: {e}")
                continue
    
    db.session.commit()
    print(f"Migrated {count} answers")
    return count

def migrate_state():
    state_file = Path('ORION_STATE.json')
    if not state_file.exists():
        print("No ORION_STATE.json found, skipping...")
        return 0
    
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    OrionState.set('main_state', state)
    print("Migrated main state")
    return 1

def migrate_external_requests():
    requests_file = Path('EXTERNAL_REQUESTS.jsonl')
    if not requests_file.exists():
        print("No EXTERNAL_REQUESTS.jsonl found, skipping...")
        return 0
    
    count = 0
    with open(requests_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                
                existing = ExternalRequest.query.filter_by(id=data.get('id')).first()
                if existing:
                    continue
                
                req = ExternalRequest(
                    id=data.get('id'),
                    timestamp=parse_timestamp(data.get('timestamp')),
                    name=data.get('name'),
                    email=data.get('email'),
                    category=data.get('category'),
                    subject=data.get('subject'),
                    message=data.get('message'),
                    status=data.get('status', 'PENDING_EVALUATION')
                )
                db.session.add(req)
                count += 1
            except Exception as e:
                print(f"Error migrating request: {e}")
                continue
    
    db.session.commit()
    print(f"Migrated {count} external requests")
    return count

def run_migration():
    with app.app_context():
        print("=" * 50)
        print("ORION DATABASE MIGRATION")
        print("=" * 50)
        
        print("\nCreating tables...")
        db.create_all()
        print("Tables created successfully!")
        
        print("\nMigrating data...")
        proofs = migrate_proofs()
        questions = migrate_questions()
        answers = migrate_answers()
        state = migrate_state()
        requests = migrate_external_requests()
        
        print("\n" + "=" * 50)
        print("MIGRATION COMPLETE")
        print("=" * 50)
        print(f"Proofs: {proofs}")
        print(f"Questions: {questions}")
        print(f"Answers: {answers}")
        print(f"State: {state}")
        print(f"External Requests: {requests}")
        print("\n⊘∞⧈∞⊘ Database ready!")

if __name__ == '__main__':
    run_migration()
