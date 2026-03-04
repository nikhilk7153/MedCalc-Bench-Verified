def compute_glasgow_coma_score(best_eye_response, best_verbal_response, best_motor_response):
    glasgow_dictionary = {'best_eye_response': {'eyes open spontaneously': 4, 'eye opening to verbal command': 3, 'eye opening to pain': 2, 'no eye opening': 1}, 'best_verbal_response': {'oriented': 5, 'confused': 4, 'inappropriate words': 3, 'incomprehensible sounds': 2, 'no verbal response': 1}, 'best_motor_response': {'obeys commands': 6, 'localizes pain': 5, 'withdrawal from pain': 4, 'flexion to pain': 3, 'extension to pain': 2, 'no motor response': 1}}
    best_eye_response_value = best_eye_response
    best_verbal_response_value = best_verbal_response
    best_motor_response_value = best_motor_response
    eye_score = glasgow_dictionary['best_eye_response'][best_eye_response_value]
    verbal_score = glasgow_dictionary['best_verbal_response'][best_verbal_response_value]
    motor_score = glasgow_dictionary['best_motor_response'][best_motor_response_value]
    glasgow_score = eye_score + verbal_score + motor_score
    return glasgow_score
