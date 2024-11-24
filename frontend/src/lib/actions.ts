import axios from "axios";

const server = "https://b739-147-232-172-153.ngrok-free.app";

export const submitFiles = async (template: File) => {
    try {
        const formData = new FormData();
        formData.append("template", template);

        return await axios.post(`${server}/process_pdf`, formData);
    } catch (e) {
        console.error(e);
    }
}

export const initAnalysis = async (files: File[]) => {
    try {
        return await axios.post(`${server}/analysis`, files);
    } catch (e) {
        console.error(e);
    }
}