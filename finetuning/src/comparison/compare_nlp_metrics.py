from rouge_score import rouge_scorer

from bert_score import score

from nltk.translate.bleu_score import (
    sentence_bleu,
    SmoothingFunction,
)


class CompareNLPMetrics:

    def __init__(self):

        self.rouge = rouge_scorer.RougeScorer(

            [

                "rouge1",

                "rouge2",

                "rougeL",

            ],

            use_stemmer=True,

        )

        self.smoothing = SmoothingFunction().method1

    def calculate(

        self,

        prediction,

        reference,

    ):

        # =====================================================
        # BLEU
        # =====================================================

        bleu = sentence_bleu(

            [

                reference.split(),

            ],

            prediction.split(),

            smoothing_function=self.smoothing,

        )

        # =====================================================
        # ROUGE
        # =====================================================

        rouge_scores = self.rouge.score(

            reference,

            prediction,

        )

        # =====================================================
        # BERTScore
        # =====================================================

        _, _, f1 = score(

            [

                prediction,

            ],

            [

                reference,

            ],

            lang="en",

            verbose=False,

        )

        return {

            "bleu": round(

                float(bleu),

                4,

            ),

            "rouge1": round(

                float(rouge_scores["rouge1"].fmeasure),

                4,

            ),

            "rouge2": round(

                float(rouge_scores["rouge2"].fmeasure),

                4,

            ),

            "rougeL": round(

                float(rouge_scores["rougeL"].fmeasure),

                4,

            ),

            "bertscore": round(

                float(f1[0]),

                4,

            ),

        }


compare_nlp_metrics = CompareNLPMetrics()