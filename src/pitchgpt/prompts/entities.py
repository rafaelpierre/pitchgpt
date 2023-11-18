template = """

Assume you are an expert in music. Please perform Named Entity Recognition (NER) manually,
without any external models, over the passage of text below, and extract all the musical
entities from it, such as: artists, music styles, album names, song names, band members,
and so on:

{review}

Please output the result as a markdown block (```python) containing a list of tuples.
Each tuple should have the classified entity, where it starts (nth character in the passage),
where it ends (nth character in the passage), and which entity is it.

Don't include any additional commentary in the output, only the markdown.
"""