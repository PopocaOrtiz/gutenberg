import { useState } from 'react';
import {createUser} from "../../utils/api.ts";

export default function Signup() {

    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>("");
    const [userId, setUserId] = useState<string>();

    const createAccount = async () => {
        const response = await createUser();
        if (response.error) {
            setError(response.error);
        } else {
            setUserId(response.data?.user_id);
        }
    }

    const signup = () => {
        setLoading(true);
        createAccount().finally(() => setLoading(false));
    }

    if (loading) {
        return <article aria-busy="true" />;
    }

    if (error) {
        return <mark>{error}</mark>
    }

    if (userId) {
        return (
            <>
                <h3>Account Id:</h3>
                <div><mark>{userId}</mark></div>
                <small>save it to login later</small>
            </>
        );
    }

    return (<>
        <input type="button"
               value="sign-up"
            onClick={() => signup()} />
    </>);
}