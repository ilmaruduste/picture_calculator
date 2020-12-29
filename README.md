# Picture Calculator
Sille Habakukk, Ilmar Uduste

## Idea
Create a script that, when given an input of a picture, could recognize mathematical operations from the picture, then calculate the whole thing and print out the final result.

This project was made in the 2020/2021 Autumn semester for a course on Artificial Intelligence (LTAT.01.003) in the University of Tartu.

## Stages of Operation
<ol>
    <li>Train an AI that could recognize numbers and basic math symbols in a picture.</li>
        <ol>
            <li>The dataset for pictures of numbers should be MNIST.</li>
            <li>TODO: We should get a dataset for basic math symbols.</li>
            <li>Try out different neural networks, RandomForestClassifiers etc.</li>
            <li>Save the model file.</li>
        </ol>
    <li>Import the trained model into the main Python script.</li>
    <li>Ask the user to import a picture containing numbers and math symbols into the main Python script via GUI.</li>
    <li>Find & classify the numbers/math symbols in the picture (AI and OpenCV).</li>
    <li>Convert the numbers and symbols into a python mathematical operation.</li>
    <li>Print the mathematical operation </li>
</ol>