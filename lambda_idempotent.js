const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB({ apiVersion: '2012-08-10' });
const limit = 8;

exports.handler = (event, context, cb) => {
    const date = new Date().toISOString().slice(0, 10);
    const id = 'iteration2:${event.user}:${date}';
    dynamodb.updateItem({
        TableName: 'rate_limit',
        Key: {
            id: { S: id },
        },
        UpdateExpression: 'ADD requests :requests', // add request to the requests set
        ConditionExpression: 'attribute_not_exists (requests) OR contains(requests, :request) OR size(requests) < :limit', // only if requests set does not exists or request is already in set or less than $limit requests in set 
        ExpressionAttributeValues: {
            ':request': { S: event.request },
            ':requests': { SS: [event.request] },
            ':limit': { N: limit.toString() }
        }
    }, function (err) {
        if (err) {
            if (err.code === 'ConditionalCheckFailedException') { // $limit requests in set and current request is not in set 
                cb(null, { limited: true });
            } else {
                cb(err);
            }
        } else {
            cb(null, { limited: false });
        }
    });
};