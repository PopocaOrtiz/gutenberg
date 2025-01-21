import {deleteSession, isLogged} from "../../store/session.ts";

export default function Title({title, description}) {

    const closeSession = () => {
        deleteSession()
        window.location = "/"
    }

    return (<>
            <header className="container">
                <hgroup>
                    {isLogged() && (
                        <small style={{'float': 'right', 'cursor': "pointer"}} onClick={() => closeSession()}>
                            cerrar session
                        </small>
                    )}
                    <h1>{title}</h1>
                    <p>{description}</p>
                </hgroup>
            </header>
        </>
    );
}