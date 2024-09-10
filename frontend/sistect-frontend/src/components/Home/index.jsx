import { useState, useContext } from "react";
import ButtonBase from "../ButtonBase";
import Nav from "../Nav";
import CadastroColab from "../CadastroColab";
import ListagemColab from "../ListagemColab";
import { HostContext } from "../../HostContext";
import './style.scss';

function get_page(page_number, usuario, setPage){
    switch(page_number){
        case 1:
            return <CadastroColab/>
        case 2:
            return <ListagemColab/>
        default:
            return <div id="btn_menu">
                <ButtonBase text="Registrar colaborador" func={{setPage}} page_number={1}/>
                <ButtonBase text="Listar colaboradores" func={{setPage}} page_number={2}/>
            </div>
    }
}

function Home({ usuario, setLoggedIn, setUsuario }) {
    const [page, setPage] = useState(0)
    const { hostUrl } = useContext(HostContext)
  
    return (
      <>
        <Nav host={hostUrl} setLoggedIn={setLoggedIn} setUsuario={setUsuario} setPage={setPage}/>
        <section id="main_content">
            {get_page(page, usuario, setPage)}
        </section>
      </>
    )
  }
  
  export default Home