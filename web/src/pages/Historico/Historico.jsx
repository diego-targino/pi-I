import { useState, useEffect } from "react";
import MenuLateral from "../MenuLateral/MenuLateral"; 
import CardPlanta from "../../components/CardPlanta"; // CORRIGIDO: Agora sobe 2 níveis e entra em components
import useAnalysisStore from "../../stores/analysisStore";
import useAuthStore from "../../stores/authStore";
import Loading from "../../components/Loading";

import iconMenu from "../../assets/images/icon-menu.png";
import logo from "../../assets/images/Logo-AnalisaAI.png";
import iconPerson from "../../assets/images/icon-person.png";

import "../Home/Home.css"; 
import "./Historico.css";

export default function Historico() {
  const [menuAberto, setMenuAberto] = useState(false); 
  const { analysisHistory, loading, error, fetchAnalysisHistory } = useAnalysisStore();
  const { user } = useAuthStore();

  useEffect(() => {
    if (user?.id) {
      fetchAnalysisHistory(user.id);
    }
  }, [user?.id]);

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

      <main>
        <div id="title-historic">
          <h2>Histórico</h2>
          <p>Confira seu histórico de pesquisa</p>
        </div>

        {/* CONTAINER DA LISTAGEM (ÚNICO) */}
        <div className="listagem-container">
          
          {loading && <Loading />}
          
          {error && (
            <div style={{ color: "#ff6b6b", textAlign: "center", padding: "20px" }}>
              <p>Erro ao carregar histórico: {error}</p>
            </div>
          )}
          
          {!loading && analysisHistory.length === 0 && (
            <div style={{ color: "#999", textAlign: "center", padding: "20px" }}>
              <p>Nenhuma análise realizada ainda</p>
            </div>
          )}

          {!loading && analysisHistory.map((planta) => (
            <CardPlanta 
              key={planta.search_request_id}
              imagem={planta.image}
              nome={planta.analysis_result?.common_name}
              descricao={planta.analysis_result?.Description}
              rotaLink={`/resultado/${planta.search_request_id}`}
            />
          ))}

        </div>
      </main>

      <MenuLateral menuAberto={menuAberto} setMenuAberto={setMenuAberto} />
    </>
  );
}