import re


class CompareMetrics:

    def calculate(

        self,

        response,

    ):

        words = len(

            response.split()

        )

        characters = len(

            response

        )

        sentences = len(

            re.findall(

                r"[.!?]+",

                response,

            )

        )

        average_word_length = (

            round(

                sum(

                    len(word)

                    for word in response.split()

                )

                / words,

                2,

            )

            if words > 0

            else 0

        )

        return {

            "words": words,

            "characters": characters,

            "sentences": sentences,

            "average_word_length": average_word_length,

        }


compare_metrics = CompareMetrics()