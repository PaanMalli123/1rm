import json

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        lift = body["lift"]
        weight = body["weight"]
        reps = body["reps"]
        unit = body["unit"]

        if reps == 1:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "https://1rm.seenikurulla.online",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                 "body": json.dumps({"message": f"No calculation needed. Your 1RM for {lift} is {weight} {unit}."})
                 }

        error = validate_input(weight, reps, lift, unit)
        if error:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "https://1rm.seenikurulla.online",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                 "body": json.dumps({"error": error})
                 }
        
        results = calculate_1rm(weight, reps)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "https://1rm.seenikurulla.online",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "lift": lift,
                "weight": weight,
                "reps": reps,
                "unit": unit,
                "results": results
            })
        }


    except Exception as e:
        print(f"Error due to: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "https://1rm.seenikurulla.online",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "An unexpected error occurred."})
        }

def validate_input(weight, reps, lift, unit):
    try:
        reps = int(reps)
        weight = float(weight)
    except (ValueError, TypeError):
        return "Reps and weight should be valid numbers."

    if unit.lower() not in ["kg", "lb"]:
        return "The input for unit does not match the specified criteria. I.e (kg/lb)"
    if lift.lower() not in ["squat", "bench" , "deadlift"]:
        return "Invalid selection for lift input"
    if weight <= 0 or weight > 1000:
        return "Weight should be a positive value and less than 1000 kg/lbs"
    if reps < 2 or reps > 20:
        return "The input for reps should be positive, greater than 1 and less than 20"


def calculate_1rm(weight, reps):
    epley_result = round(weight * (1 + (reps/30)),2)
    brzycki_result = round(weight * (36 / (37 - reps)),2)
    lander_result = round((100 * weight) / (101.3 - (2.67123 * reps)), 2)
    final_1rm = round(((epley_result + brzycki_result + lander_result) / 3), 2)
    return {
        "epley": epley_result,
        "brzycki": brzycki_result,
        "lander": lander_result,
        "average": final_1rm
    }

