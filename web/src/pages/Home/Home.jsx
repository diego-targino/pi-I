import { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import "./Home.css";

// Importação dos componentes
import MenuLateral from "../MenuLateral/MenuLateral";
import Loading from "../../components/Loading";

// Imagens do projeto
import logo from "../../assets/images/Logo-AnalisaAI.png";
import iconMenu from "../../assets/images/icon-menu.png";
import iconPerson from "../../assets/images/icon-person.png";
import iconSelecionar from "../../assets/images/icon-selecionar.png";
import { toBase64 } from "../../utils/converter";
import useAnalysisStore from "../../stores/analysisStore";
import useAuthStore  from "../../stores/authStore";

export default function Home() {
  const [menuAberto, setMenuAberto] = useState(false);
  const [imagemPreview, setImagemPreview] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [imageBase64, setImageBase64] = useState("");
  const { createAnalysis, searchRequestId ,analysis, loading, error } = useAnalysisStore();
    const { user } = useAuthStore();
  const navigate = useNavigate();

  const aoSelecionarFoto = async (event) => {
    const arquivo = event.target.files[0];
    if (arquivo) {
      const urlTemporaria = URL.createObjectURL(arquivo);
      setImagemPreview(urlTemporaria);
      setImageBase64(await toBase64(arquivo)); 
    }
  };

  const escolherOutraFoto = () => {
    setImagemPreview(null);
  };

  const confirmarEnvio = async (e) => {
    e.preventDefault();
    try{
      setCarregando(true); 
      await createAnalysis(imageBase64, user.id); 
      setCarregando(false); 

      if(analysis && searchRequestId){
        navigate(`/retorno/${searchRequestId}`, { 
          state: { imagemUrl: imagemPreview } 
        });
      }
    }

    catch(err){
      alert("Erro ao analisar a planta");
      return;
    }
  };

  return (
    <>
      <header>
        <div id="cabecalho">
          <img
            id="icon-menu"
            src={iconMenu}
            alt="Menu"
            onClick={() => setMenuAberto(true)}
          />
          <img id="logo" src={logo} alt="Logo" />
          <img id="icon-person" src={iconPerson} alt="Perfil" />
        </div>
      </header>

      <MenuLateral menuAberto={menuAberto} setMenuAberto={setMenuAberto} />

      <main>
        <div id="corpo">
          
          {carregando ? (
            <Loading />
          ) : (
            <>
              {!imagemPreview ? (
                <div id="container-selecao">
                  <h2>Envie uma foto agora mesmo e analise a sua planta</h2>

                  <div id="selecionar">
                    <img
                      id="photo-selection"
                      src={iconSelecionar}
                      alt="Selecionar"
                    />

                    <input
                      type="file"
                      id="gerenciadorArquivos"
                      accept=".jpg, .jpeg, .png"
                      style={{ display: "none" }}
                      onChange={aoSelecionarFoto} 
                    />

                    <label htmlFor="gerenciadorArquivos" id="arquivo" style={{ cursor: "pointer" }}>
                      Selecionar arquivo
                    </label>
                  </div>

                  <div id="recomendacao">
                    <div className="bloco">
                      <li>Envie uma foto com iluminação clara</li>
                      <li>Evite fotos tremidas ou fora de foco</li>
                      <li>Garante que a foto não esteja borrada</li>
                    </div>
                    <div className="bloco">
                      <li>Aproxime a câmera da folha ou da área afetada</li>
                      <li>Mostre apenas uma planta por foto</li>
                      <li>Evite outras plantas ou objetos misturados no fundo</li>
                    </div>
                  </div>
                </div>
              ) : (
                <div id="container-confirmacao">
                  <h2>Sua foto ficou assim:</h2>
                  
                  <div className="preview-box">
                    <img id="preview-foto" src={imagemPreview} alt="Sua planta" />
                  </div>

                  <div className="botoes-confirmacao">
                    <button id="btn-confirmar" onClick={confirmarEnvio}>Analisar Planta</button>
                    <button id="btn-alterar" onClick={escolherOutraFoto}>Escolher Outra</button>
                  </div>
                </div>
              )}
            </>
          )}

        </div>
      </main>
    </>
  );
}