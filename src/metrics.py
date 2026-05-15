import time
import math
import re
from typing import Dict, Any, List
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from textblob import TextBlob
    HAS_ML_LIBS = True
except ImportError:
    HAS_ML_LIBS = False


class DebateEvaluator:
    """
    A lightweight, professional observability and evaluation layer for the 
    Multi-Agent Debate Architecture.
    
    This class captures metrics related to agent performance, debate quality,
    system efficiency, and human-readability without requiring heavy external models.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.start_time = time.time()
        self.end_time = None
        self.metrics = {}

    def calculate_readability(self, text: str) -> float:
        """
        Calculates a rough Flesch Reading Ease score.
        Higher score = easier to read.
        """
        if not text:
            return 0.0
        
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]
        
        if len(words) == 0 or len(sentences) == 0:
            return 0.0

        # Rough syllable estimation
        vowels = "aeiouy"
        syllables = 0
        for word in words:
            word = word.lower()
            count = 0
            if word[0] in vowels:
                count += 1
            for index in range(1, len(word)):
                if word[index] in vowels and word[index - 1] not in vowels:
                    count += 1
            if word.endswith("e"):
                count -= 1
            if count == 0:
                count += 1
            syllables += count

        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
        return round(max(0.0, min(100.0, score)), 2)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculates cosine similarity between two texts using TF-IDF.
        Useful for measuring diversity and contribution.
        """
        if not HAS_ML_LIBS or not text1 or not text2:
            return 0.0
        
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return round(float(similarity), 4)
        except Exception:
            return 0.0

    def analyze_sentiment(self, text: str) -> float:
        """
        Returns sentiment polarity from -1.0 (negative) to 1.0 (positive).
        """
        if not HAS_ML_LIBS or not text:
            return 0.0
        return round(TextBlob(text).sentiment.polarity, 4)

    def estimate_tokens(self, text: str) -> int:
        """
        Standard heuristic: 1 token is roughly 4 English characters.
        """
        if not text:
            return 0
        return len(text) // 4

    def evaluate(self, optimist_out: str, risk_out: str, moderator_out: str) -> Dict[str, Any]:
        """
        Runs the full evaluation suite on the outputs of the debate crew.
        """
        self.end_time = time.time()
        total_latency = round(self.end_time - self.start_time, 2)

        # 1. SYSTEM PERFORMANCE
        tokens_opt = self.estimate_tokens(optimist_out)
        tokens_risk = self.estimate_tokens(risk_out)
        tokens_mod = self.estimate_tokens(moderator_out)
        total_tokens = tokens_opt + tokens_risk + tokens_mod

        # 2. CORE AGENT PERFORMANCE (Length & Sentiment)
        sentiment_opt = self.analyze_sentiment(optimist_out)
        sentiment_risk = self.analyze_sentiment(risk_out)
        sentiment_mod = self.analyze_sentiment(moderator_out)

        # 3. MULTI-AGENT DEBATE METRICS
        # Diversity Score: How different are Optimist and Risk Analyst? (Lower similarity = higher diversity)
        similarity_opt_risk = self.calculate_similarity(optimist_out, risk_out)
        debate_diversity_score = round(1.0 - similarity_opt_risk, 4)

        # Agent Contribution Score: How much did each agent influence the Moderator's final verdict?
        contrib_opt = self.calculate_similarity(optimist_out, moderator_out)
        contrib_risk = self.calculate_similarity(risk_out, moderator_out)
        
        # Normalize contributions to percentages
        total_contrib = contrib_opt + contrib_risk
        if total_contrib > 0:
            opt_influence = round((contrib_opt / total_contrib) * 100, 2)
            risk_influence = round((contrib_risk / total_contrib) * 100, 2)
        else:
            opt_influence = 50.0
            risk_influence = 50.0

        # Consensus Quality: High if the moderator considered both reasonably well (closer to 50/50 is better balance)
        consensus_quality = round(100.0 - abs(opt_influence - risk_influence), 2)

        # 4. HUMAN QUALITY METRICS
        readability_mod = self.calculate_readability(moderator_out)

        # 5. RELIABILITY (Heuristics)
        # Logical Consistency: A rough heuristic checking if the moderator structured their output
        logical_consistency = 100 if ("1." in moderator_out and "2." in moderator_out) else 50

        self.metrics = {
            "System_Performance": {
                "Total_Latency_Seconds": total_latency,
                "Estimated_Total_Tokens": total_tokens,
                "Estimated_Cost_USD": round((total_tokens / 1000) * 0.001, 5) # Assuming very rough $0.001 per 1k tokens
            },
            "Core_Agent_Performance": {
                "Optimist_Tokens": tokens_opt,
                "Risk_Analyst_Tokens": tokens_risk,
                "Moderator_Tokens": tokens_mod,
                "Optimist_Sentiment": sentiment_opt,
                "Risk_Analyst_Sentiment": sentiment_risk,
                "Moderator_Sentiment": sentiment_mod
            },
            "Debate_Quality": {
                "Debate_Diversity_Score": debate_diversity_score, # Closer to 1.0 means highly distinct viewpoints
                "Optimist_Contribution_Influence": f"{opt_influence}%",
                "Risk_Analyst_Contribution_Influence": f"{risk_influence}%",
                "Consensus_Quality_Score": consensus_quality # Closer to 100 means perfectly balanced synthesis
            },
            "Human_Readability": {
                "Moderator_Readability_Score": readability_mod, # 0-100 (higher is easier to read)
                "Logical_Consistency_Score": logical_consistency # Basic structural check
            }
        }

        return self.metrics

    def get_formatted_report(self) -> str:
        """
        Returns a beautifully formatted string representation of the metrics
        for terminal or UI display.
        """
        if not self.metrics:
            return "No metrics generated yet."

        report = "\n" + "="*50 + "\n"
        report += "📊 AI OBSERVABILITY & EVALUATION REPORT\n"
        report += "="*50 + "\n"
        
        for category, data in self.metrics.items():
            report += f"\n--- {category.replace('_', ' ').upper()} ---\n"
            for key, value in data.items():
                formatted_key = key.replace('_', ' ')
                report += f"{formatted_key}: {value}\n"
        
        report += "="*50 + "\n"
        return report
