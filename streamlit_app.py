import random
import streamlit as st

# 중학생 수준 영단어 데이터베이스
VOCABULARY = {
    "apple": "사과",
    "book": "책",
    "cat": "고양이",
    "dog": "개",
    "elephant": "코끼리",
    "friend": "친구",
    "happy": "행복한",
    "house": "집",
    "music": "음악",
    "orange": "주황색",
    "parent": "부모",
    "question": "질문",
    "river": "강",
    "school": "학교",
    "teacher": "선생님",
    "umbrella": "우산",
    "video": "영상",
    "water": "물",
    "yellow": "노란색",
    "zoo": "동물원",
    "beautiful": "아름다운",
    "computer": "컴퓨터",
    "dance": "춤",
    "eight": "8",
    "family": "가족",
    "green": "초록색",
    "holiday": "휴일",
    "ice": "얼음",
    "jump": "뛰다",
    "kitchen": "부엌",
    "library": "도서관",
    "medicine": "약",
    "nose": "코",
    "office": "사무실",
    "phone": "전화",
    "quiet": "조용한",
    "rainbow": "무지개",
    "sister": "누나/언니",
    "tired": "피곤한",
    "uncle": "삼촌",
    "voice": "목소리",
    "window": "창문",
}


def init_session_state():
    """세션 상태 초기화"""
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "menu"
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "total_questions" not in st.session_state:
        st.session_state.total_questions = 0
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []


def generate_meaning_quiz(num_questions=10):
    """의미 맞추기 문제 생성"""
    words = random.sample(list(VOCABULARY.items()), num_questions)
    quiz_data = []

    for word, meaning in words:
        options = [meaning]
        wrong_options = random.sample([m for w, m in VOCABULARY.items() if w != word], 3)
        options.extend(wrong_options)
        random.shuffle(options)

        quiz_data.append(
            {
                "word": word,
                "correct": meaning,
                "options": options,
                "type": "meaning",
            }
        )

    return quiz_data


def generate_spelling_quiz(num_questions=10):
    """철자 맞추기 문제 생성"""
    words = random.sample(list(VOCABULARY.keys()), num_questions)
    quiz_data = []

    for word in words:
        quiz_data.append({"word": word, "meaning": VOCABULARY[word], "type": "spelling"})

    return quiz_data


def display_meaning_quiz():
    """의미 맞추기 게임 표시"""
    st.header("📚 의미 맞추기")
    st.write(f"점수: {st.session_state.score} / {st.session_state.total_questions}")

    if st.session_state.current_question < len(st.session_state.quiz_data):
        quiz = st.session_state.quiz_data[st.session_state.current_question]

        st.markdown(f"### 질문 {st.session_state.current_question + 1}/{len(st.session_state.quiz_data)}")
        st.markdown(f"## **{quiz['word'].upper()}** 의 뜻은?")

        selected = st.radio("선택지:", quiz["options"], key=f"q_{st.session_state.current_question}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ 확인", use_container_width=True):
                if selected == quiz["correct"]:
                    st.success("🎉 정답입니다!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 틀렸습니다. 정답: {quiz['correct']}")

                st.session_state.current_question += 1
                st.rerun()

        with col2:
            if st.button("⏭️ 다음문제", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
    else:
        st.success("🎊 게임 완료!")
        st.write(f"### 최종 점수: {st.session_state.score} / {st.session_state.total_questions}")

        if st.button("🏠 영단어 페이지로 돌아가기", use_container_width=True):
            st.session_state.game_mode = "menu"
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.rerun()


def display_spelling_quiz():
    """철자 맞추기 게임 표시"""
    st.header("🔤 철자 맞추기")
    st.write(f"점수: {st.session_state.score} / {st.session_state.total_questions}")

    if st.session_state.current_question < len(st.session_state.quiz_data):
        quiz = st.session_state.quiz_data[st.session_state.current_question]

        st.markdown(f"### 질문 {st.session_state.current_question + 1}/{len(st.session_state.quiz_data)}")
        st.markdown(f"## **{quiz['meaning']}** 을 영어로?")

        user_answer = st.text_input(
            "답을 입력하세요 (영문):",
            key=f"spelling_{st.session_state.current_question}",
            placeholder="예: apple",
        ).strip().lower()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ 확인", use_container_width=True):
                if user_answer == quiz["word"]:
                    st.success("🎉 정답입니다!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ 틀렸습니다. 정답: {quiz['word']}")

                st.session_state.current_question += 1
                st.rerun()

        with col2:
            if st.button("⏭️ 다음문제", use_container_width=True):
                st.session_state.current_question += 1
                st.rerun()
    else:
        st.success("🎊 게임 완료!")
        st.write(f"### 최종 점수: {st.session_state.score} / {st.session_state.total_questions}")

        if st.button("🏠 영단어 페이지로 돌아가기", use_container_width=True):
            st.session_state.game_mode = "menu"
            st.session_state.score = 0
            st.session_state.current_question = 0
            st.rerun()


def render_vocabulary_page():
    """영단어 학습 페이지"""
    st.header("📚 영단어 공부")
    st.write("영단어를 보고 뜻을 익힌 뒤, 게임으로 복습해 보세요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 의미 맞추기 게임", use_container_width=True):
            st.session_state.quiz_data = generate_meaning_quiz(10)
            st.session_state.total_questions = 10
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.game_mode = "meaning"
            st.rerun()

    with col2:
        if st.button("🔤 철자 맞추기 게임", use_container_width=True):
            st.session_state.quiz_data = generate_spelling_quiz(10)
            st.session_state.total_questions = 10
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.game_mode = "spelling"
            st.rerun()

    st.subheader("💡 오늘의 단어")
    word, meaning = random.choice(list(VOCABULARY.items()))
    st.info(f"**{word}**: {meaning}")

    with st.expander("📖 단어장 보기"):
        cols = st.columns(2)
        for i, (word, meaning) in enumerate(sorted(VOCABULARY.items())):
            with cols[i % 2]:
                st.write(f"**{word}** - {meaning}")


def render_bts_page():
    """BTS 소개 페이지"""
    st.header("🎤 BTS 소개")
    st.write("BTS는 한국의 대표적인 보이 그룹으로, 멋진 음악과 강한 메시지로 많은 사람들에게 사랑받고 있습니다.")

    st.success("BTS는 7명의 멤버로 이루어져 있고, 글로벌 인기를 얻은 그룹입니다.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👑 대표 멤버")
        st.write("- RM: 그룹 리더")
        st.write("- Jin: 부드러운 목소리로 유명")
        st.write("- Suga: 랩과 작사로 활약")
        st.write("- J-Hope: 밝고 에너지 넘치는 춤")

    with col2:
        st.subheader("🎵 대표곡")
        st.write("- Dynamite")
        st.write("- Butter")
        st.write("- Boy With Luv")
        st.write("- Permission to Dance")

    st.subheader("✨ BTS가 특별한 이유")
    st.markdown(
        "- 멋진 춤과 노래를 선보입니다.\n"
        "- 의미 있는 가사로 많은 사람들에게 감동을 줍니다.\n"
        "- 전 세계 팬들과 함께 성장하는 그룹입니다."
    )


def main():
    """메인 함수"""
    st.set_page_config(page_title="영단어와 BTS 앱", page_icon="🎮", layout="centered")

    init_session_state()

    st.title("🎯 영어 공부 + BTS")
    st.write("영단어를 공부하고 BTS를 알아보세요.")

    tab_vocabulary, tab_bts = st.tabs(["📚 영단어", "🎤 BTS"])

    with tab_vocabulary:
        if st.session_state.game_mode == "menu":
            render_vocabulary_page()
        elif st.session_state.game_mode == "meaning":
            display_meaning_quiz()
        elif st.session_state.game_mode == "spelling":
            display_spelling_quiz()

    with tab_bts:
        render_bts_page()


if __name__ == "__main__":
    main()
