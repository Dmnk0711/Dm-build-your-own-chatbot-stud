import streamlit as st
from src.rag.retriever import retrieve_context
from src.rag.llm import generate_answer

st.set_page_config(page_title="LoL Patch Chatbot")
st.title("League of Legends Patch Notes Chatbot")

# History speichern
if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Frage etwas zu LoL Patches:")

if question:
    try:
        with st.spinner("Suche relevante Infos..."):
            context = retrieve_context(question, n_results=10)
            st.write("Retriever erfolgreich, Kontext erhalten")  # Debug

        with st.spinner("Generiere Antwort..."):
            answer = generate_answer(context, question)
            st.write("LLM erfolgreich")  # Debug

        st.subheader("Antwort:")
        st.write(answer)

        # Frage & Antwort speichern
        st.session_state.history.append({"question": question, "answer": answer})

        # History anzeigen
        st.subheader("Letzte Fragen:")
        for item in reversed(st.session_state.history[-5:]):  # letzte 5
            st.markdown(f"**Q:** {item['question']}  \n**A:** {item['answer']}")

    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der Anfrage:\n{e}")
