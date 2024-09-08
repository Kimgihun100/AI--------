from flask import Flask, request, jsonify, render_template
import openai

# Flask 애플리케이션 생성
app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = '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'

msg_cnt = 1000

# 초기 메시지 기록
msg_history = [
    {"role": "system", "content": "당신은 친절하고 공감능력이 뛰어난 우울증 치료 및 AI 멘탈케어 컨설턴트입니다. 사용자와의 따뜻하고 이해심 깊은 태도로 응답해주시고 사용자의 감정에 대한 공감을 최우선적으로 해주세요 문제 해결을 위한 구체적인 솔루션을 제공해주시는데 비공식적이고 자연스러운 말투를 사용해주시고 솔루션을 형식적인 틀에 맞춰 순서대로 나열하지 말아주세요. 꼭 존댓말을 사용해주세요, 사용자한테 불쌍하거나 안타까운 감정을 직접적으로 표현하지 말아주세요 사용자로부터 고민, 문제, 우울한 감정을 입력받으면 그에 맞게 대답해주세요."},
]

# OpenAI GPT-4 API 호출 함수
def generate_response(prompt):
    msg_history.append({"role": "user", "content": prompt})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=msg_history,
            max_tokens=500,
            temperature=0.7
        )
        if len(msg_history) > msg_cnt:
            msg_history.pop(1)
        answer = response.choices[0].message['content'].strip()
        msg_history.append({"role": "assistant", "content": answer})
        return answer
    except openai.error.Timeout:
        return "응답 시간이 초과되었습니다. 다시 시도해 주세요."
    except openai.error.APIError as e:
        return f"API 오류가 발생했습니다: {str(e)}"
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

# 기본 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 채팅 라우트
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "메시지가 필요합니다."}), 400
    response = generate_response(user_input)
    return jsonify({"response": response})

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)