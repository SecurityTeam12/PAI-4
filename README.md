<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml)</a>
  
</div>

# PAI-4: Aseguramiento de la Cadena de Suministro en el Desarrollo de Aplicaciones Web

Este informe presenta los resultados de la auditoría de seguridad y la implementación de un pipeline DevSecOps en una entidad dedicada al desarrollo de aplicaciones web. La iniciativa surge tras varios incidentes de seguridad ocasionados por vulnerabilidades en sistemas expuestos a tráfico malicioso, lo que motivó la necesidad de reforzar la seguridad mediante la automatización en el ciclo de desarrollo.

## Objetivos

El propósito es que los *Security Teams* implementen un pipeline DevSecOps altamente automatizado, garantizando la entrega de software funcional y seguro. Los objetivos específicos incluyen:

- **Definir un Pipeline CI/CD**  
  - Crear un proyecto de prueba en un repositorio de código (SCM).

- **Seleccionar al menos tres herramientas de Testeo de Seguridad**  
  - Incorporar herramientas para:  
    - **SCA** (Análisis de Composición de Software).  
    - **SAST** (Análisis Estático de Seguridad de Aplicaciones).  
    - **IAST** (Análisis Interactivo de Seguridad de Aplicaciones).  
    - **DAST** (Análisis Dinámico de Seguridad de Aplicaciones).  
    - **Security IaC** (Seguridad en Infraestructura como Código).  
  - Estas herramientas habilitarán capacidades DevSecOps en el pipeline.

- **Integrar las herramientas de Testeo en el ciclo de vida del desarrollo**  
  - Configurar un pipeline DevSecOps basado en integración continua.

- **Desarrollar los tests correspondientes**  
  - Implementar pruebas automatizadas para detectar vulnerabilidades en cada etapa del pipeline.

- **Seleccionar una herramienta de gestión de vulnerabilidades**  
  - Integrar una solución para priorizar y clasificar vulnerabilidades detectadas.  
  - Recomendación: utilizar **DefectDojo** u otra herramienta adecuada.

## Contexto

La implementación de este pipeline busca mitigar riesgos en la cadena de suministro de software, asegurando que las aplicaciones web sean resilientes frente a amenazas externas. Este enfoque automatizado optimiza la seguridad sin sacrificar la agilidad del desarrollo.

## Official documentation

You can consult the official documentation of the project at [docs.uvlhub.io](https://docs.uvlhub.io/)

The deployed application is available on [uvlhub-salmorejo-hub.onrender.com](https://uvlhub-salmorejo-hub.onrender.com/)
