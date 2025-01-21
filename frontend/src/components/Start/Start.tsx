import Signup from "../Signup/Signup.tsx";
import Login from "../Login/Login.tsx";

function Start() {
    return (<article>
        <form>
            <h3>Start here:</h3>
            <div>
                <Login />
            </div>
            <div>
                <Signup/>
            </div>
        </form>
    </article>);
}

export default Start;