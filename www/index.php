<?php
$page = $_SERVER['PHP_SELF'];
$sec = "10";
$pdo = new PDO('mysql:host=localhost;port=$dbport=3306;dbname=SAE', "SAE", "DBPassword");
$pdo->exec("SET CHARACTER SET utf8");
$stmt = $pdo->prepare("SELECT * FROM environment ORDER BY timestamp DESC LIMIT 1"); # merci https://stackoverflow.com/questions/5191503/how-to-select-the-last-record-of-a-table-in-sql
$stmt->execute();
$res = $stmt->fetchAll();
$louistemp = $res[0]["louistemp"];
$louishum = $res[0]["louishum"];
$paweltemp = $res[0]["paweltemp"];
$pawelhum = $res[0]["pawelhum"];
$owmtemp = $res[0]["owmtemp"];
$owmhum = $res[0]["owmhum"];
$stmt = $pdo->prepare("SELECT * FROM system_usage ORDER BY timestamp DESC LIMIT 1");
$stmt->execute();
$res = $stmt->fetchAll();
$louisCPU = $res[0]["louisCPU"];
$louisRAM = $res[0]["louisRAM"];
$pawelCPU = $res[0]["pawelCPU"];
$pawelRAM = $res[0]["pawelRAM"];
$stmt = $pdo->prepare("SELECT * FROM power_data ORDER BY timestamp DESC LIMIT 1");
$stmt->execute();
$res = $stmt->fetchAll();
$louisPAPP = $res[0]["louisPAPP"];
$pawelPAPP = $res[0]["pawelPAPP"];
$pdo = null;
date_default_timezone_set('Europe/Paris');
?>
<!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'">
        <link rel="stylesheet" href="style.css">
        <script src="print.js"></script>
        <title>SAE203</title>
    </head>
    <body>
        <h1>SAE203</h1>
        <p><?php echo date("Y-m-d H:i:s"); ?></p>
        <button id="printBtn" class="btn-print">Imprimer</button>
        <div id="print">
            <section class="print-block">
                <h2>meteo</h2>
                <table>
                    <tr>    
                        <th>temperature</th>
                        <th>humidité</th>
                    </tr>
                    <tr>
                        <th>
                            <!-- https://stackoverflow.com/questions/8749434/how-to-prevent-browser-image-caching  -->
                            <img src=<?php echo "graph/Température.png?t=".time();?> width="500" height="300">
                            <table>
                                <tr><th>Louis:</th><th>Pawel:</th><th>Exterieur:</th></tr>
                                <tr><th><?php echo $louistemp; ?>°C</th><th><?php echo $paweltemp; ?>°C</th><th><?php echo $owmtemp; ?>°C</th></tr> 
                            </table>
                        </th>
                        <th>
                            <img src=<?php echo "graph/Humidité.png?t=".time();?> width="500" height="300">
                            <table>
                                <tr><th>Louis:</th><th>Pawel:</th><th>Exterieur:</th></tr>
                                <tr><th><?php echo $louishum; ?>%</th><th><?php echo $pawelhum; ?>%</th><th><?php echo $owmhum; ?>%</th></tr> 
                            </table>
                        </th>
                    </tr>
                </table>
            </section>
            <section class="print-block">
                <h2>info serveur</h2>
                <table>
                    <tr>    
                        <th>Chez Louis</th>
                        <th>Chez Pawel</th>
                    </tr>
                    <tr>
                        <th>
                            <img src=<?php echo "graph/ServeurLouis.png?t=".time();?> width="500" height="300">
                            <table>
                                <tr><th>RAM:</th><th>CPU:</th></tr>
                                <tr><th><?php echo $louisRAM; ?>%</th><th><?php echo $louisCPU; ?>%</th></tr>
                            </table>
                        </th>   
                        <th>
                            <img src=<?php echo "graph/ServeurPawel.png?t=".time();?> width="500" height="300">
                            <table>
                                <tr><th>RAM:</th><th>CPU:</th></tr>
                                <tr><th><?php echo $pawelRAM; ?>%</th><th><?php echo $pawelCPU; ?>%</th></tr> 
                            </table>
                        </th>
                    </tr>
                </table>
            </section>
            <section class="print-block">
                <h2>Consommation electrique (puissance apparente)</h2>
                <table>
                    <tr>    
                        <th>Chez Louis (Sortie onduleur du serveur)</th>
                        <th>Chez Pawel (Linky de l'appartement)</th>
                    </tr>
                    <tr>
                        <th>
                            <img src=<?php echo "graph/ConsoServeurLouis.png?t=".time();?> width="500" height="300">
                            <p><?php echo $louisPAPP; ?> VA</p>
                        </th>
                        <th>
                            <img src=<?php echo "graph/LinkyPawel.png?t=".time();?> width="500" height="300">
                            <p><?php echo $pawelPAPP; ?> VA</p>
                        </th>
                    </tr>
                </table>
            </section>
        </div>
    </body>
</html>
