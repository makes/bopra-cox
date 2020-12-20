<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>Assessing autoregulation using cerebral oximetry in a prehospital setting</title>
    <meta name="description" content="Research page.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <!--link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"-->
</head>

<body>

    <?php
    include("Parsedown.php");

    $page = "markdown/8_images.md";
    if (isset($_GET['page'])) $page = "markdown/" . $_GET['page'] . ".md";

    $Parsedown = new Parsedown();

    echo $Parsedown->text(file_get_contents($page));
    ?>

</body>

</html>