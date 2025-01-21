import {useState} from "react";
import {saveSession} from "../../store/session.ts";

export default function Login() {

    const [showInput, setShowInput] = useState(false);
    const [userId, setUserId] = useState("");

    const login = async () => {
        saveSession(userId);
    }
    if (showInput) {
        return (<>
            <fieldset role="group">
                <input type="text"
                       onChange={(e) => setUserId(e.target.value)}
                       value={userId}/>
                <input onClick={() => login()}
                       type="submit"
                       value="enter"/>
            </fieldset>
        </>);
    }

    return (
        <input onClick={() => setShowInput(true)}
               type="button"
               value="login"/>
    );
}