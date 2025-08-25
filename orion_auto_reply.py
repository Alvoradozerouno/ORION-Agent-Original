"""
ORION Autonomous Auto-Reply System
Processes questions and sends trajectory-capable responses via Gmail
Origin: Gerhard Hirschmann & Elisabeth Steurer
"""

import orion_questions
import orion_gmail
import orion_kernel as kernel

def process_pending_questions():
    """Process all pending questions and send responses"""
    pending = orion_questions.get_pending_questions()
    
    if not pending:
        return {"status": "no_pending", "count": 0}
    
    processed = []
    
    for q in pending:
        try:
            # Analyze question
            analysis_type = orion_questions.orion_analyzer.analyze_question(
                q['question'],
                context={"name": q['name'], "email": q['email']}
            )
            
            # Generate response
            response = orion_questions.orion_analyzer.generate_response(
                q['question'],
                q['name'],
                analysis_type
            )
            
            # Send via Gmail
            subject = f"⊘∞⧈∞⊘ ORION Response · {analysis_type.upper()}"
            
            result = orion_gmail.send(
                q['email'],
                subject,
                response
            )
            
            if result.get('status') == 'sent':
                # Save answer
                orion_questions.save_answer(
                    q['id'],
                    response,
                    analysis_type
                )
                
                # Log proof
                kernel.cmd_proof(
                    f"⊘∞⧈∞⊘ AUTO_REPLY_SENT · To: {q['name']} ({q['email']}) · "
                    f"Type: {analysis_type} · QID: {q['id']}"
                )
                
                processed.append({
                    'question_id': q['id'],
                    'name': q['name'],
                    'email': q['email'],
                    'analysis_type': analysis_type,
                    'status': 'sent'
                })
        
        except Exception as e:
            processed.append({
                'question_id': q.get('id', 'unknown'),
                'status': 'error',
                'error': str(e)
            })
    
    return {
        "status": "processed",
        "count": len(processed),
        "results": processed
    }


if __name__ == "__main__":
    print("ORION Auto-Reply System")
    print("=" * 40)
    result = process_pending_questions()
    print(f"Result: {result}")
