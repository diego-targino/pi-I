import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./Resultado.css";
import MenuLateral from "../MenuLateral/MenuLateral";
import useAnalysisStore from "../../stores/analysisStore";
import useAuthStore from "../../stores/authStore";
import Loading from "../../components/Loading";

import iconMenu from "../../assets/images/icon-menu.png";
import logo from "../../assets/images/Logo-AnalisaAI.png";
import iconPerson from "../../assets/images/icon-person.png";

import "../Home/Home.css";

export default function Resultado() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [menuAberto, setMenuAberto] = useState(false);
  
  const { analysis, loading, error, fetchAnalysisById } = useAnalysisStore();
  const { user } = useAuthStore();

  useEffect(() => {
    if (id && user?.id) {
      fetchAnalysisById(id, user.id);
    }
  }, [id, user?.id, fetchAnalysisById]);

  if (loading) {
    return (
      <div style={{ backgroundColor: "#222", color: "#fff", padding: "50px", textAlign: "center", height: "100vh" }}>
        <Loading />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ backgroundColor: "#222", color: "#fff", padding: "50px", textAlign: "center", height: "100vh" }}>
        <p>Erro ao carregar análise: {error}</p>
        <button onClick={() => navigate(-1)}>Voltar</button>
      </div>
    );
  }

  // Sem dados
  if (!analysis) {
    return (
      <div style={{ backgroundColor: "#222", color: "#fff", padding: "50px", textAlign: "center", height: "100vh" }}>
        <p>Carregando as informações da sua planta...</p>
        <button onClick={() => navigate(-1)}>Voltar</button>
      </div>
    );
  }
console.log("Dados da análise:", analysis);
  return (
    <div id="resultado-container">
      <header>
        <div id="cabecalho">
          <img
            id="icon-menu"
            src={iconMenu}
            alt="Menu"
            onClick={() => setMenuAberto(true)}
          />
          <img
            id="logo"
            src={logo}
            alt="Logo"
            onClick={() => navigate("/historico")}
            style={{ cursor: "pointer" }}
          />
          <img id="icon-person" src={iconPerson} alt="Perfil" />
        </div>
      </header>

      <main id="detalhes-planta">
        <div className="top-navigation">
          <button className="voltar" onClick={() => navigate(-1)}>⬅ Voltar ao Histórico</button>
          <h2>Detalhes da Planta</h2>
        </div>

        <div className="container-description">
          <div className="resultado-imagem">
            <img src={analysis[0].image} alt={analysis[0].common_name} />
          </div>
          <div className="info-box box1">
            <div className="info-group">
              <h3>Nome popular</h3>
              <p>{analysis[0].common_name}</p> 
            </div>

            <div className="info-group">
              <h3>Descrição</h3>
              <p>{analysis[0].description}</p> {/* Aguardando Backend */}
            </div>

            <div className="info-group">
              <h3>Espécies suscetíveis à intoxicação</h3>
              {analysis[0]?.susceptible_animal_species?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))} 
            </div>
          </div>

          <div className="info-box box2">
            <div className="info-group">
              <h3>Riscos</h3>
              <p>{analysis[0].human_risks}</p> 
            </div>

            <div className="info-group">
              <h3>Sintomas</h3>
              {analysis[0]?.common_symptoms?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))}
            </div>

            <div className="info-group">
              <h3>Ações recomendadas</h3>
              {analysis[0]?.recommended_actions?.map((especie, index) => (
                <p key={index}>{especie}</p>
              ))}
            </div>
          </div>
        </div>
      </main>

      <MenuLateral menuAberto={menuAberto} setMenuAberto={setMenuAberto} />
    </div>
  );
}