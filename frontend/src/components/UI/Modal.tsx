export default function Modal({ onClose, title, children}) {
    return (<dialog open>
        <article>
            <header>
                <button onClick={() => onClose()}
                        aria-label="Close"
                        rel="prev"></button>
                <p>
                    <strong>{title}</strong>
                </p>
            </header>
            {children}
        </article>
    </dialog>);
}