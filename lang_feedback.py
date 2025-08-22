import language_tool_python

def generate_feedback(text, lang='en'):
    """
    Analyze IELTS reading/writing answers and return feedback.
    'en' for English, 'ar' for Arabic, 'both' for combined
    """
    feedback_list = []
    sentences = text.split('.')
    
    tools = {}
    if lang in ['en', 'both']:
        tools['en'] = language_tool_python.LanguageTool('en-US')
        tools['en'].enable_only('GRAMMAR', 'STYLE', 'TYPOGRAPHY', 'REDUNDANCY')  # IELTS focus
    if lang in ['ar', 'both']:
        tools['ar'] = language_tool_python.LanguageTool('ar')
    
    if not tools:
        raise ValueError("Unsupported language")
    
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        issues = []
        for tool_lang, tool in tools.items():
            matches = tool.check(sent)
            for match in matches:
                issue_dict = {
                    'sentence': sent,
                    'issue': match.category.lower().capitalize(),  # E.g., 'Grammar', 'Style'
                    'tip': match.message,  # E.g., 'Did you mean "an"?'
                    'translation_tip': ''  # Placeholder for bilingual feedback
                }
                
                # Add suggestions if available, limit to 2 for clarity
                if match.replacements:
                    issue_dict['tip'] += f" Suggestion: {', '.join(match.replacements[:2])}"
                
                # Customize tips for IELTS clarity
                if match.category == 'GRAMMAR':
                    issue_dict['tip'] += " (Check verb tense, articles, or agreement for academic writing)"
                elif match.category == 'STYLE':
                    issue_dict['tip'] += " (Use formal language for IELTS writing)"
                elif match.category == 'REDUNDANCY':
                    issue_dict['tip'] += " (Simplify for clarity in IELTS responses)"
                
                # Bilingual tip (simple pseudo-translation; enhance with googletrans if needed)
                if tool_lang == 'en' and match.message:
                    issue_dict['translation_tip'] = f"ترجمة: {issue_dict['tip']}"
                
                issues.append(issue_dict)
        
        feedback_list.extend(issues)
    
    for tool in tools.values():
        tool.close()
    return feedback_list