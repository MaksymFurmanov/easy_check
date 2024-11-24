import axios from "axios";

const server = "http://127.0.0.1:5000";

export const submitFiles = async (template: File, files: File[]) => {
    const data = {
        template,
        files
    }

    console.log(data);

    try {
        return await axios.post(`${server}/data`, data);
    } catch (e) {
        console.error(e);
    }
}