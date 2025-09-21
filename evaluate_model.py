#!/usr/bin/env python3
"""
Model Performance Evaluation for Ama Arogya ChatBot
This script evaluates various aspects of the ChatBot model performance.
"""
import requests
import json
import time
from typing import List, Dict, Tuple


class ChatBotEvaluator:
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.test_cases = self.get_test_cases()

    def get_test_cases(self) -> List[Dict]:
        """Define test cases for evaluation"""
        return [
            # Fever Detection Tests
            {"message": "I have fever", "language": "en", "expected_topic": "fever"},
            {"message": "मुझे बुखार है", "language": "hi", "expected_topic": "fever"},
            {"message": "ମୋର ଜ୍ବର ଅଛି", "language": "or", "expected_topic": "fever"},
            {"message": "my temperature is high",
                "language": "en", "expected_topic": "fever"},

            # Headache Detection Tests
            {"message": "I have headache", "language": "en",
                "expected_topic": "headache"},
            {"message": "मेरे सिर में दर्द है",
                "language": "hi", "expected_topic": "headache"},
            {"message": "ମୋର ମାଥା ବଥା", "language": "or",
                "expected_topic": "headache"},

            # Cough Detection Tests
            {"message": "I have cough", "language": "en", "expected_topic": "cough"},
            {"message": "मुझे खांसी है", "language": "hi", "expected_topic": "cough"},
            {"message": "throat pain", "language": "en", "expected_topic": "cough"},

            # Pregnancy Tests
            {"message": "I am pregnant", "language": "en",
                "expected_topic": "pregnancy"},
            {"message": "गर्भावस्था की जानकारी",
                "language": "hi", "expected_topic": "pregnancy"},
            {"message": "maternal care", "language": "en",
                "expected_topic": "pregnancy"},

            # Vaccination Tests
            {"message": "vaccination schedule", "language": "en",
                "expected_topic": "vaccination"},
            {"message": "टीकाकरण", "language": "hi",
                "expected_topic": "vaccination"},
            {"message": "vaccine information", "language": "en",
                "expected_topic": "vaccination"},

            # Stomach Pain Tests
            {"message": "stomach pain", "language": "en",
                "expected_topic": "stomach_pain"},
            {"message": "पेट में दर्द", "language": "hi",
                "expected_topic": "stomach_pain"},
            {"message": "belly ache", "language": "en",
                "expected_topic": "stomach_pain"},

            # General/Unknown Tests
            {"message": "hello", "language": "en", "expected_topic": "general"},
            {"message": "how are you", "language": "en",
                "expected_topic": "general"},
            {"message": "what is your name", "language": "en",
                "expected_topic": "general"},
        ]

    def test_single_case(self, test_case: Dict) -> Dict:
        """Test a single case and return results"""
        try:
            start_time = time.time()

            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "message": test_case["message"],
                    "sender_id": "eval_user",
                    "language": test_case["language"]
                },
                timeout=10
            )

            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # ms

            if response.status_code == 200:
                result = response.json()
                detected_intent = result.get("intent", "unknown")

                # Check if detection is correct
                correct = (detected_intent == test_case["expected_topic"]) or \
                    (test_case["expected_topic"] == "general" and detected_intent in [
                     "general", "cached"])

                return {
                    "success": True,
                    "correct": correct,
                    "message": test_case["message"],
                    "language": test_case["language"],
                    "expected": test_case["expected_topic"],
                    "detected": detected_intent,
                    "response": result.get("response", ""),
                    "response_time": response_time,
                    "server_response_time": result.get("response_time_ms", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "message": test_case["message"]
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": test_case["message"]
            }

    def run_evaluation(self) -> Dict:
        """Run complete evaluation and return metrics"""
        print("Starting ChatBot Model Evaluation...")
        print("=" * 50)

        results = []
        correct_detections = 0
        total_tests = len(self.test_cases)
        response_times = []
        language_accuracy = {"en": {"correct": 0, "total": 0},
                             "hi": {"correct": 0, "total": 0},
                             "or": {"correct": 0, "total": 0}}

        for i, test_case in enumerate(self.test_cases, 1):
            print(f"Testing {i}/{total_tests}: {test_case['message'][:30]}...")

            result = self.test_single_case(test_case)
            results.append(result)

            if result.get("success"):
                response_times.append(result.get("response_time", 0))
                lang = test_case["language"]
                language_accuracy[lang]["total"] += 1

                if result.get("correct"):
                    correct_detections += 1
                    language_accuracy[lang]["correct"] += 1
                    print(f"  ✅ Correct: {result.get('detected')}")
                else:
                    print(
                        f"  ❌ Wrong: Expected {result.get('expected')}, Got {result.get('detected')}")
            else:
                print(f"  ❌ Failed: {result.get('error')}")

        # Calculate metrics
        accuracy = (correct_detections / total_tests) * \
            100 if total_tests > 0 else 0
        avg_response_time = sum(response_times) / \
            len(response_times) if response_times else 0

        # Language-specific accuracy
        lang_scores = {}
        for lang, stats in language_accuracy.items():
            if stats["total"] > 0:
                lang_scores[lang] = (stats["correct"] / stats["total"]) * 100
            else:
                lang_scores[lang] = 0

        return {
            "overall_accuracy": accuracy,
            "total_tests": total_tests,
            "correct_detections": correct_detections,
            "failed_tests": total_tests - len([r for r in results if r.get("success")]),
            "average_response_time": avg_response_time,
            "language_accuracy": lang_scores,
            "detailed_results": results
        }

    def print_evaluation_report(self, metrics: Dict):
        """Print a detailed evaluation report"""
        print("\n" + "=" * 60)
        print("         AMA AROGYA CHATBOT - MODEL EVALUATION REPORT")
        print("=" * 60)

        # Overall Score
        overall_score = metrics["overall_accuracy"]
        print(f"\n🎯 OVERALL MODEL SCORE: {overall_score:.1f}%")

        # Grade the model
        if overall_score >= 90:
            grade = "A+ (Excellent)"
        elif overall_score >= 80:
            grade = "A (Very Good)"
        elif overall_score >= 70:
            grade = "B (Good)"
        elif overall_score >= 60:
            grade = "C (Fair)"
        else:
            grade = "D (Needs Improvement)"

        print(f"📊 MODEL GRADE: {grade}")

        # Detailed Metrics
        print(f"\n📈 DETAILED METRICS:")
        print(f"   • Total Test Cases: {metrics['total_tests']}")
        print(f"   • Correct Detections: {metrics['correct_detections']}")
        print(f"   • Failed Tests: {metrics['failed_tests']}")
        print(
            f"   • Success Rate: {((metrics['total_tests'] - metrics['failed_tests']) / metrics['total_tests'] * 100):.1f}%")
        print(
            f"   • Average Response Time: {metrics['average_response_time']:.2f}ms")

        # Language Performance
        print(f"\n🌐 LANGUAGE-SPECIFIC PERFORMANCE:")
        for lang, accuracy in metrics["language_accuracy"].items():
            lang_names = {"en": "English", "hi": "Hindi", "or": "Odia"}
            print(f"   • {lang_names.get(lang, lang)}: {accuracy:.1f}%")

        # Performance Categories
        print(f"\n🎯 PERFORMANCE ANALYSIS:")
        topic_performance = self.analyze_topic_performance(
            metrics["detailed_results"])
        for topic, stats in topic_performance.items():
            if stats["total"] > 0:
                accuracy = (stats["correct"] / stats["total"]) * 100
                print(
                    f"   • {topic.replace('_', ' ').title()}: {accuracy:.1f}% ({stats['correct']}/{stats['total']})")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if overall_score >= 80:
            print("   ✅ Model performance is good for production use")
            print("   ✅ Consider adding more advanced NLP features")
        elif overall_score >= 60:
            print("   ⚠️  Model needs improvement in topic detection")
            print("   ⚠️  Consider expanding keyword patterns")
        else:
            print("   ❌ Model needs significant improvement")
            print("   ❌ Review detection algorithms and add more training data")

        print("\n" + "=" * 60)

    def analyze_topic_performance(self, results: List[Dict]) -> Dict:
        """Analyze performance by topic"""
        topic_stats = {}

        for result in results:
            if result.get("success"):
                expected = result.get("expected", "unknown")
                correct = result.get("correct", False)

                if expected not in topic_stats:
                    topic_stats[expected] = {"correct": 0, "total": 0}

                topic_stats[expected]["total"] += 1
                if correct:
                    topic_stats[expected]["correct"] += 1

        return topic_stats


def main():
    evaluator = ChatBotEvaluator()

    # Check if server is running
    try:
        response = requests.get(f"{evaluator.base_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running or not healthy!")
            print("Please start the server with: python main.py")
            return
    except:
        print("❌ Cannot connect to server!")
        print("Please make sure the server is running at http://127.0.0.1:8001")
        return

    # Run evaluation
    metrics = evaluator.run_evaluation()
    evaluator.print_evaluation_report(metrics)


if __name__ == "__main__":
    main()
