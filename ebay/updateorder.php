<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
$client = new SoapClient('http://staging.esupplybox.com/api/soap/?wsdl', array('trace' => 1));
$session = $client->login('test', 'tester');

$params = array(
    'item_id' => 9059,
    'order_id' => 7368,
    'ebay_transaction_id' => '-',
    'trackig_id' => 'Issue In Item Page',
    'tracking_url' => 'cyz',
);

$result = $client->call($session, 'neworders.update', $params);
echo "<pre>";
print_r($result);
exit();
?>