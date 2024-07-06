<?php
require_once __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;
use Symfony\Component\DomCrawler\Crawler;

// Global vars 
$client = new Client();
$booksOfTheBible = [
    // Old Testament
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra",
    "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations",
    "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk",
    "Zephaniah", "Haggai", "Zechariah", "Malachi",
    
    // New Testament
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
    "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
];
$booksKeyed = [];
$crossRefsCSV = fopen('cross-refs.csv', 'w');
if (!$crossRefsCSV) die ('There was an issue opening cross-refs.csv.');

readCsvLineByLine('niv.csv');

function readCsvLineByLine(string $fileName) {
    if (!file_exists($fileName) || !is_readable($fileName)) {
        echo "The file $fileName does not exist or is not readable.";
        return;
    }

    $totalLines = countLines($fileName);

    // Open the file in read mode
    if (($handle = fopen($fileName, 'r')) !== false) {
        $lineCount = 0;
        // Loop through each line in the file
        while (($line = fgetcsv($handle, 1000, ',')) !== false) {
            processLine($line, $lineCount);
            $lineCount++;
            displayProgressBar($lineCount, $totalLines);
        }
        // Close the file
        fclose($handle);
    } else {
        echo "Error opening the file $fileName.";
    }
}

function processLine(array $line) {
    global $booksOfTheBible, $client;

    $verse = $line[2];
    $chapter = $line[1];
    $book = $booksOfTheBible[$line[0] - 1];

    $response = $client->get("https://www.openbible.info/labs/cross-references/search?q=$book+$chapter+$verse");
    $html = (string) $response->getBody();
    $crawler = new Crawler($html);
    $crossRefs = $crawler->filterXPath('//div[contains(@class, "crossrefs")]/div[not(contains(@class, "crossref-verse"))]')->each(function (Crawler $node, $i) use ($book, $chapter, $verse, $line) {
        global $booksOfTheBible, $booksKeyed, $crossRefsCSV;

        $modifier = 0;
        $info = preg_split("/[\s:-]+/", $node->filterXPath('//h3')->text());
        if (intval($info[0])) {
            $info[0] = $info[0] . ' ' . $info[1];
            $modifier = 1;
        }

        if (!($referenceBook = $booksKeyed[$info[0]] ?? false)) {
            $referenceBook = array_search($info[0], $booksOfTheBible) + 1;
            $booksKeyed[$info[0]] = $referenceBook;
        }

        $referenceChapter = $info[1 + $modifier];
        $referenceStartVerse = $info[2 + $modifier];
        $referenceEndVerse = $info[3 + $modifier] ?? 0;
        $referenceText = $node->filterXPath('//p')->text();

        fputcsv($crossRefsCSV, [$line[0], $chapter, $verse, $referenceBook, $referenceChapter, $referenceStartVerse, $referenceEndVerse, $referenceText]);
    });
}

function countLines($fileName) {
    $lineCount = 0;
    $handle = fopen($fileName, "r");
    while(!feof($handle)){
        fgets($handle);
        $lineCount++;
    }

    fclose($handle);
    return $lineCount;
}

function displayProgressBar($current, $total, $barLength = 50) {
    $progress = ($current / $total);
    $filledLength = round($barLength * $progress);
    $bar = str_repeat('█', $filledLength) . str_repeat('-', $barLength - $filledLength);

    $percent = round($progress * 100, 2);
    echo "\r|$bar| $percent% Complete";
    if ($current === $total) echo "\n";
}
?>
