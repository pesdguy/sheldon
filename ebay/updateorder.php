<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$client = new SoapClient('http://staging.esupplybox.com/api/soap/?wsdl', array('trace' => 1));
$session = $client->login('test', 'tester');

if(defined('STDIN'))  {
    $params = array(
        'item_id' => $argv[1],
        'order_id' => $argv[2],
        'ebay_transaction_id' => $argv[3],
        'trackig_id' => $argv[4],
        'tracking_url' => $argv[5],
    );

    $result = $client->call($session, 'neworders.update', $params);
    echo "<pre>";
    print_r($result);
} else  {
    echo 'Argument Not Found';
}
exit();
?>