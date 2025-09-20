import streamlit as st
import re
import random
from typing import List, Dict, Tuple

class AssignmentQuizGenerator:
    def __init__(self):
        self.assignment_templates = [
            "Write a comprehensive essay analyzing {topic}. Discuss its key components, significance, and implications.",
            "Compare and contrast different aspects of {topic}. Provide specific examples and explain their relevance.",
            "Evaluate the importance of {topic} in its broader context. Support your arguments with evidence and reasoning.",
            "Examine the relationship between {topic} and related concepts. How do they influence each other?",
            "Create a detailed analysis of {topic}, including its causes, effects, and potential solutions or applications."
        ]
        
        self.question_starters = [
            "What is the main concept behind",
            "Which of the following best describes",
            "What are the key characteristics of",
            "Which statement is most accurate about",
            "What is the primary purpose of"
        ]
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from the input text."""
        # Clean and normalize text
        text = re.sub(r'[^\w\s]', ' ', text)
        sentences = text.split('.')
        
        concepts = []
        
        # Extract noun phrases and important terms
        words = text.split()
        
        # Look for capitalized words (potential proper nouns/concepts)
        for word in words:
            if word.capitalize() == word and len(word) > 3:
                concepts.append(word.lower())
        
        # Extract frequent meaningful words (longer than 4 characters)
        word_freq = {}
        for word in words:
            clean_word = word.lower().strip()
            if len(clean_word) > 4 and clean_word.isalpha():
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Add most frequent words as concepts
        frequent_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        concepts.extend([word for word, freq in frequent_words if freq > 1])
        
        # Remove duplicates and return unique concepts
        return list(set(concepts))[:8]  # Limit to top 8 concepts
    
    def generate_assignments(self, text: str, concepts: List[str]) -> List[str]:
        """Generate assignment questions based on text and concepts."""
        assignments = []
        
        if concepts:
            # Use top concepts for assignments
            selected_concepts = concepts[:2] if len(concepts) >= 2 else concepts
            
            for i, concept in enumerate(selected_concepts):
                template = self.assignment_templates[i % len(self.assignment_templates)]
                assignment = template.format(topic=concept.title())
                assignments.append(assignment)
        
        # If we don't have enough concepts, generate generic assignments
        while len(assignments) < 2:
            remaining_templates = [t for t in self.assignment_templates if not any(t in a for a in assignments)]
            if remaining_templates:
                template = random.choice(remaining_templates)
                generic_topic = "the main topic discussed"
                assignment = template.format(topic=generic_topic)
                assignments.append(assignment)
            else:
                break
        
        return assignments[:2]
    
    def generate_quiz_questions(self, text: str, concepts: List[str]) -> List[Dict]:
        """Generate multiple choice quiz questions."""
        questions = []
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        
        # Generate questions based on concepts and text content
        for i in range(3):
            if i < len(concepts):
                concept = concepts[i]
                question_start = random.choice(self.question_starters)
                question = f"{question_start} {concept}?"
                
                # Generate answer options
                correct_answer = f"{concept.title()} is a key concept discussed in the text"
                
                wrong_answers = [
                    f"{concept.title()} is not mentioned in the context",
                    f"{concept.title()} is only briefly referenced",
                    f"{concept.title()} is contradicted by the main argument"
                ]
                
                # Add some variation to wrong answers
                if i == 1:
                    wrong_answers = [
                        f"{concept.title()} has no practical applications",
                        f"{concept.title()} is an outdated concept",
                        f"{concept.title()} is purely theoretical"
                    ]
                elif i == 2:
                    wrong_answers = [
                        f"{concept.title()} is the least important aspect",
                        f"{concept.title()} is a minor detail",
                        f"{concept.title()} is incorrectly defined"
                    ]
                
            else:
                # Generate more generic questions if we run out of concepts
                question = f"Based on the text, which statement is most accurate?"
                correct_answer = "The text provides valuable information on the topic"
                wrong_answers = [
                    "The text contradicts itself frequently",
                    "The text lacks any coherent structure",
                    "The text is purely fictional"
                ]
            
            # Randomize answer order
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            correct_index = all_answers.index(correct_answer)
            
            questions.append({
                'question': question,
                'options': all_answers,
                'correct_answer': chr(65 + correct_index)  # Convert to A, B, C, D
            })
        
        return questions

def main():
    st.set_page_config(
        page_title="Assignment & Quiz Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Assignment & Quiz Generator")
    st.markdown("Generate educational assignments and quizzes from any text or topic!")
    
    # Initialize the generator
    generator = AssignmentQuizGenerator()
    
    # Sidebar for input
    with st.sidebar:
        st.header("📝 Input Options")
        
        input_method = st.radio(
            "Choose input method:",
            ["Text Input", "Topic Input"]
        )
        
        if input_method == "Text Input":
            input_text = st.text_area(
                "Paste your document or text:",
                placeholder="Enter the text you want to generate assignments and quizzes from...",
                height=200
            )
        else:
            topic = st.text_input(
                "Enter a topic:",
                placeholder="e.g., Photosynthesis, World War II, Machine Learning"
            )
            
            if topic:
                # Generate sample text from topic
                input_text = f"""
                {topic} is an important subject that involves multiple key concepts and principles. 
                Understanding {topic} requires knowledge of its fundamental components, processes, and applications.
                The study of {topic} encompasses various aspects including its historical development, 
                current applications, and future implications. Key elements of {topic} include its 
                theoretical foundations, practical implementations, and relationship to other related fields.
                Researchers and practitioners in {topic} continue to explore new methodologies and 
                approaches to advance our understanding of this important area.
                """
            else:
                input_text = ""
        
        generate_button = st.button("🚀 Generate Content", type="primary")
    
    # Main content area
    if generate_button and input_text.strip():
        with st.spinner("Generating assignments and quiz questions..."):
            # Extract key concepts
            concepts = generator.extract_key_concepts(input_text)
            
            # Generate assignments
            assignments = generator.generate_assignments(input_text, concepts)
            
            # Generate quiz questions
            quiz_questions = generator.generate_quiz_questions(input_text, concepts)
        
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📋 Assignments", "❓ Quiz Questions", "🔍 Analysis"])
        
        with tab1:
            st.header("📋 Assignment Questions")
            for i, assignment in enumerate(assignments, 1):
                st.subheader(f"Assignment {i}")
                st.write(assignment)
                st.markdown("---")
        
        with tab2:
            st.header("❓ Multiple Choice Quiz")
            for i, q in enumerate(quiz_questions, 1):
                st.subheader(f"Question {i}")
                st.write(q['question'])
                
                for j, option in enumerate(q['options']):
                    label = chr(65 + j)  # A, B, C, D
                    st.write(f"**{label}.** {option}")
                
                st.success(f"**Correct Answer:** {q['correct_answer']}")
                st.markdown("---")
        
        with tab3:
            st.header("🔍 Content Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Text Statistics")
                word_count = len(input_text.split())
                sentence_count = len([s for s in input_text.split('.') if s.strip()])
                
                st.metric("Word Count", word_count)
                st.metric("Sentence Count", sentence_count)
                st.metric("Concepts Identified", len(concepts))
            
            with col2:
                st.subheader("🏷️ Key Concepts")
                if concepts:
                    for concept in concepts:
                        st.tag(concept.title())
                else:
                    st.info("No specific concepts identified")
    
    elif generate_button:
        st.warning("⚠️ Please provide some input text or topic to generate content.")
    
    else:
        # Default state - show instructions
        st.markdown("""
        ## How to use this tool:
        
        1. **Choose your input method** in the sidebar:
           - **Text Input**: Paste a document or text content
           - **Topic Input**: Enter a topic name for automatic content generation
        
        2. **Click "Generate Content"** to create:
           - 2 assignment questions (essay prompts)
           - 3 multiple-choice quiz questions with answers
           - Content analysis and key concepts
        
        ## Features:
        - 📝 **Smart Assignment Generation**: Creates essay prompts based on extracted concepts
        - ❓ **Multiple Choice Quizzes**: Generates questions with 4 options each
        - 🔍 **Content Analysis**: Shows text statistics and identified key concepts
        - 🎯 **Flexible Input**: Works with documents, articles, or simple topic names
        
        ---
        *Start by entering your text or topic in the sidebar!*
        """)

if __name__ == "__main__":
    main()
