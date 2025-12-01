<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP + React MFE  – Product Journeys</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 24px;
            background-color: #f5f5f5;
        }

        h1 {
            margin-bottom: 16px;
        }

        .cards-container {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            margin-bottom: 24px;
        }

        .card {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            padding: 16px 20px;
            flex: 1 1 280px;
            max-width: 380px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .card-header {
            margin-bottom: 12px;
        }

        .card-title {
            font-size: 18px;
            font-weight: bold;
            margin: 0 0 4px 0;
        }

        .card-subtitle {
            font-size: 13px;
            color: #666666;
            margin: 0;
        }

        .card-body {
            font-size: 14px;
            color: #444444;
            margin-bottom: 12px;
        }

        .card-footer {
            display: flex;
            justify-content: flex-end;
        }

        .btn-primary {
            padding: 8px 14px;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            background-color: #0066cc;
            color: #ffffff;
            font-size: 13px;
        }

        .btn-primary:hover {
            background-color: #004f99;
        }

        .mfe-container {
            margin-top: 32px;
            padding: 16px;
            border-radius: 8px;
            background-color: #ffffff;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
            min-height: 120px;
        }

        .mfe-placeholder {
            color: #999;
            font-size: 13px;
        }
    </style>
</head>
<body>

    <h1>Your Products</h1>

    <div class="cards-container">
        <!-- Insurance Card -->
        <div class="card">
            <div class="card-header">
                <p class="card-title">Insurance</p>
                <p class="card-subtitle">Protection for your life & assets</p>
            </div>
            <div class="card-body">
                <p>
                    View and manage your insurance policy details, coverage,
                    and claims journeys. This will launch the Insurance React MFE.
                </p>
            </div>
            <div class="card-footer">
                <a href="#" class="btn-primary"
                        onclick="loadJourney('SAML_INS_123')">
                    View Details
            </a>
            </div>
        </div>
    
        <!-- Investment Card -->
        <div class="card">
            <div class="card-header">
                <p class="card-title">Investment</p>
                <p class="card-subtitle">Track and grow your investments</p>
            </div>
            <div class="card-body">
                <p>
                    View your portfolios, performance charts, and perform
                    investment journeys. This will launch the Investment React MFE.
                </p>
            </div>
            <div class="card-footer">
                <a href="#" class="btn-primary"
                        onclick="loadJourney('SAML_INV_456')">
                    View Details
            </a>
            </div>
        </div>
    </div>

<!-- <ul>
    <li>
        Insurance Product
        <a href="#" onclick="loadJourney('SAML_INS_123')">View Details</a>
    </li>
    <li>
        Investment Product
        <a href="#" onclick="loadJourney('SAML_INV_456')">View Details</a>
    </li>
</ul> -->

<hr/>

<div id="react-product-root"></div>

<script>
    let loaderScriptLoaded = false;

    function loadJourney(samlToken) {
        const root = document.getElementById('react-product-root');
        root.dataset.samlToken = samlToken;

        if (!loaderScriptLoaded) {
            const script = document.createElement('script');
            script.type = 'module';
            script.src = 'http://localhost:4400/loader.js'; // universal-loader dev
            script.onload = function () {
                loaderScriptLoaded = true;
                console.log('loader.js downloaded');
            };
            script.onerror = function () {
                console.error('Failed to load loader.js');
            };
            document.body.appendChild(script);
        } else {
            if (window.UniversalLoader && window.UniversalLoader.run) {
                window.UniversalLoader.run();
            }
        }
    }
</script>

</body>
</html>
