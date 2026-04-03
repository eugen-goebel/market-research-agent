"""
Mock data for --dry-run mode.

Provides realistic AnalysisResult instances so the full pipeline
(report generation, DOCX output, styling) can be tested without an API key.
"""

from .analyst import AnalysisResult, SWOTAnalysis, Competitor


SAP_MOCK = AnalysisResult(
    executive_summary=(
        "SAP SE is the world's leading provider of enterprise application software, "
        "with over 400,000 customers in 180 countries. The company has successfully "
        "pivoted from on-premise ERP to a cloud-first model, with cloud revenue now "
        "representing over 40% of total sales. Despite intense competition from Oracle "
        "and Salesforce, SAP maintains a dominant position in core ERP, with its S/4HANA "
        "platform driving a multi-year migration cycle across its installed base."
    ),
    company_overview=(
        "SAP SE was founded in 1972 in Walldorf, Germany, by five former IBM engineers. "
        "Today, headquartered in Walldorf, Baden-Württemberg, it employs over 105,000 people "
        "worldwide and generates approximately €31 billion in annual revenue. SAP's product "
        "portfolio spans ERP (S/4HANA), CRM (Salesforce competitor: SAP CX), supply chain "
        "(SAP IBP), HR management (SuccessFactors), and business intelligence (SAP Analytics "
        "Cloud). The company serves large enterprises and mid-market companies across "
        "manufacturing, retail, financial services, and the public sector."
    ),
    market_position=(
        "SAP holds a commanding ~24% share of the global ERP market and is widely regarded "
        "as the system of record for core business processes at Fortune 500 companies. Its "
        "competitive moat stems from deep integration complexity — replacing SAP is a "
        "multi-year, high-risk transformation that most enterprises avoid. SAP's RISE with SAP "
        "offering bundles S/4HANA Cloud with managed services, accelerating cloud migration. "
        "The company targets €21.5 billion in cloud revenue by 2025, indicating a fundamental "
        "shift in its business model toward recurring subscription income."
    ),
    swot=SWOTAnalysis(
        strengths=[
            "Dominant ERP market share (~24%) with extremely high switching costs",
            "400,000+ customer installed base providing stable recurring revenue",
            "Deep industry-specific solutions across 25+ verticals",
            "Strong R&D investment (~15% of revenue) driving continuous innovation",
            "Successful RISE with SAP cloud migration program gaining traction",
        ],
        weaknesses=[
            "Legacy on-premise revenue declining faster than cloud growth can compensate",
            "Complex, expensive implementation projects averaging 18–24 months",
            "User experience historically criticized as outdated compared to modern SaaS",
            "Dependence on partner ecosystem for delivery creates quality inconsistency",
            "SAP Business Suite to S/4HANA migration creates customer anxiety and churn risk",
        ],
        opportunities=[
            "Generative AI integration (Joule AI assistant) across entire product suite",
            "Untapped mid-market segment via SAP Business ByDesign and partner channels",
            "Supply chain digitalization demand accelerating post-COVID across all industries",
            "Green Ledger sustainability reporting becoming mandatory (CSRD, EU taxonomy)",
            "Business Network (Ariba, Fieldglass) expanding into B2B marketplace model",
        ],
        threats=[
            "Oracle Fusion Cloud aggressively winning SAP displacement deals",
            "Salesforce + MuleSoft offering compelling alternative for CRM + integration",
            "Microsoft Dynamics 365 gaining share in mid-market with Teams integration",
            "AI-native ERP startups (e.g., Workday for HCM) reducing SAP's edge in niches",
            "Macro slowdown delaying large transformation projects and license upgrades",
        ],
    ),
    top_competitors=[
        Competitor(
            name="Oracle Corporation",
            overview="US-based enterprise software giant offering Oracle Fusion Cloud ERP, HCM, and SCM as direct SAP competitors.",
            key_strength="Integrated technology stack (database + cloud infrastructure + applications) and aggressive cloud pricing",
            key_weakness="Perceived as complex to implement and historically reliant on hardware bundling",
        ),
        Competitor(
            name="Microsoft Dynamics 365",
            overview="Microsoft's ERP and CRM suite tightly integrated with Azure, Teams, and the Microsoft 365 ecosystem.",
            key_strength="Seamless integration with Office 365 and Azure, plus competitive mid-market pricing",
            key_weakness="Limited depth for large enterprise manufacturing and complex logistics scenarios",
        ),
        Competitor(
            name="Salesforce",
            overview="World's leading CRM platform, increasingly competing with SAP CX and expanding into ERP adjacencies via MuleSoft and Slack.",
            key_strength="Best-in-class CRM UX, massive AppExchange ecosystem, and AI (Einstein) leadership",
            key_weakness="Limited ERP core capabilities; relies on integrations for back-office processes",
        ),
        Competitor(
            name="Workday",
            overview="Cloud-native HCM and financial management platform targeting SAP SuccessFactors and SAP S/4HANA Finance.",
            key_strength="Modern cloud-native architecture, strong user adoption, and best-of-breed HR analytics",
            key_weakness="Narrower industry coverage than SAP; limited manufacturing and supply chain capabilities",
        ),
    ],
    key_trends=[
        "Generative AI embedded in ERP workflows: co-pilots, automated reconciliation, predictive maintenance",
        "Cloud ERP migration accelerating — Gartner forecasts 75% of ERP workloads in cloud by 2026",
        "Sustainability reporting mandates (EU CSRD, SEC climate disclosure) driving demand for ESG modules",
        "Supply chain resilience investments post-COVID boosting SCM and procurement software spend",
        "Rise of composable ERP: modular best-of-breed architectures challenging monolithic suites",
        "Low-code / no-code customization tools reducing dependency on expensive SI partners",
        "Data sovereignty and localization requirements (GDPR, China PIPL) shaping cloud deployment strategies",
    ],
    investment_thesis=(
        "SAP's multi-year cloud transition is approaching an inflection point, with RISE with SAP "
        "driving high-value migrations from the 400,000-strong installed base. If the company "
        "successfully embeds generative AI (Joule) across its suite and accelerates mid-market "
        "adoption, it is well-positioned to sustain double-digit cloud revenue growth while "
        "expanding operating margins as the mix shifts from license to subscription."
    ),
    risk_factors=[
        "Cloud transition cannibilizes high-margin license revenue faster than expected",
        "Oracle or Microsoft displacing SAP in key enterprise accounts during migration windows",
        "Global recession delaying large-scale ERP transformation projects by 12–24 months",
        "Integration failures or cost overruns in RISE with SAP eroding customer trust",
        "Talent competition for AI and cloud engineers increasing R&D cost base",
    ],
)


ZALANDO_MOCK = AnalysisResult(
    executive_summary=(
        "Zalando SE is Europe's leading online fashion and lifestyle platform, operating "
        "in 25 markets with over 50 million active customers. The company generated EUR 10.1 "
        "billion in gross merchandise volume (GMV) in 2024, up 3.5% year-over-year. Zalando is "
        "transitioning from a pure retailer to a platform ecosystem model (ZEOS), enabling third-party "
        "brands to leverage its logistics, payments, and customer base as a service."
    ),
    company_overview=(
        "Zalando SE was founded in 2008 in Berlin by Robert Gentz and David Schneider, initially "
        "as an online shoe retailer. Today it employs approximately 17,000 people and operates "
        "across 25 European markets. Its product portfolio spans fashion, beauty, accessories, "
        "and lifestyle categories, offering over 6,000 brands. Zalando operates its own logistics "
        "network with 12 fulfillment centers across Europe, plus a growing partner fulfillment program."
    ),
    market_position=(
        "Zalando holds approximately 11% of the European online fashion market and is the largest "
        "dedicated fashion e-commerce platform on the continent. Its competitive moat stems from "
        "brand density (6,000+ brands), logistics infrastructure (same-day/next-day delivery in "
        "key markets), and a strong mobile-first user experience. The ZEOS platform play aims to "
        "position Zalando as the operating system for European fashion commerce."
    ),
    swot=SWOTAnalysis(
        strengths=[
            "Largest European online fashion platform with 50M+ active customers",
            "Proprietary logistics network enabling fast delivery across 25 markets",
            "Strong brand partnerships with 6,000+ fashion and lifestyle labels",
            "Successful private label portfolio (Zign, YOURTURN) driving margin expansion",
        ],
        weaknesses=[
            "Profitability remains thin — adjusted EBIT margin around 2-3% historically",
            "Heavy dependence on promotional pricing and discounts to drive volume",
            "Limited presence outside Europe — no meaningful US or Asia business",
            "Returns rate of 40-50% in fashion significantly impacts unit economics",
        ],
        opportunities=[
            "ZEOS platform-as-a-service model creating new high-margin revenue streams",
            "Connected retail bridging online and offline for brand partners",
            "Pre-owned fashion and recommerce segment growing 30%+ annually",
            "AI-powered personalization improving conversion rates and reducing returns",
        ],
        threats=[
            "Shein and Temu offering ultra-low-price fashion undercutting European players",
            "Amazon Fashion investing heavily in European fashion infrastructure",
            "About You (acquired by Zalando) integration risks and execution challenges",
            "Consumer spending pressures from inflation reducing discretionary fashion spend",
        ],
    ),
    top_competitors=[
        Competitor(
            name="ASOS plc",
            overview="UK-based online fashion retailer targeting 20-somethings across Europe and globally.",
            key_strength="Strong brand identity with younger demographics and own-brand margin advantage",
            key_weakness="Struggling with profitability and operational restructuring since 2023",
        ),
        Competitor(
            name="Amazon Fashion",
            overview="Amazon's fashion vertical leveraging its massive logistics network and Prime membership base.",
            key_strength="Unmatched logistics scale, Prime flywheel, and limitless category expansion",
            key_weakness="Perceived as less curated and fashion-forward compared to dedicated platforms",
        ),
        Competitor(
            name="About You",
            overview="Hamburg-based fashion platform recently acquired by Zalando, previously a direct competitor.",
            key_strength="Strong personalization engine and younger customer demographic in DACH region",
            key_weakness="Persistent losses and now being integrated into Zalando ecosystem",
        ),
        Competitor(
            name="H&M Group (Online)",
            overview="Swedish fast-fashion giant with growing e-commerce operations across 60+ markets.",
            key_strength="Massive physical store network complementing online presence with omnichannel strategy",
            key_weakness="Brand perception challenges around sustainability and fast-fashion criticism",
        ),
    ],
    key_trends=[
        "Platform business models replacing pure retail — Zalando ZEOS, Farfetch, marketplace shifts",
        "AI-driven personalization and virtual try-on reducing return rates by 15-20%",
        "Recommerce and circular fashion growing as sustainability regulation tightens",
        "Social commerce integration (TikTok Shop, Instagram Shopping) reshaping discovery",
        "Quick commerce pressure — consumer expectations shifting to same-day delivery",
        "Direct-to-consumer brands bypassing platforms with Shopify-powered storefronts",
        "EU Digital Services Act and sustainability reporting mandates increasing compliance costs",
    ],
    investment_thesis=(
        "Zalando's transition to a platform model via ZEOS has the potential to unlock significantly "
        "higher margins than its traditional retail business. With 50M+ active customers and a dominant "
        "logistics network, it is well positioned to become the Shopify of European fashion. The About You "
        "acquisition adds scale, but integration execution remains the key near-term risk."
    ),
    risk_factors=[
        "ZEOS platform adoption by brands slower than projected, limiting margin uplift",
        "Shein/Temu price competition eroding market share in price-sensitive segments",
        "About You integration consuming management attention and creating operational friction",
        "Fashion returns rate (40-50%) structurally limiting profitability improvement",
        "European consumer spending downturn reducing discretionary fashion purchases",
    ],
)


COMPARISON_MOCKS = {
    "SAP SE": SAP_MOCK,
    "Zalando SE": ZALANDO_MOCK,
}
