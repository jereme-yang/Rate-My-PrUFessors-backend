import { DynamoDBClient, GetItemCommand } from "@aws-sdk/client-dynamodb";
import { unmarshall } from "@aws-sdk/util-dynamodb";

const client = new DynamoDBClient({});

export async function handler(event) {
  const profname = event?.queryStringParameters?.profname;

  if (!profname) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing "name" query parameter' }),
    };
  }

  const command = new GetItemCommand({
    TableName: "rmp-gatorevals",
    Key: {
      profname: { S: profname },
    },
  });

  try {
    const result = await client.send(command);

    if (!result.Item) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: `No entry found for "${profname}"` }),
      };
    }

    const item = unmarshall(result.Item);

    return {
      statusCode: 200,
      body: JSON.stringify({ data: item }),
    };
  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: err.message }),
    };
  }
}
